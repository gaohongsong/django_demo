# -*- coding: utf-8 -*-
"""
    CBV - class based view
    在DRF中使用类式视图的样例
"""
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import mixins, generics, renderers, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

import django_filters
from snippets.filters import SnippetFilter

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer, SnippetSerializer1
from snippets.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


# ==============================================APIView===================================================
class SnippetList(APIView):
    """
    查询snippets列表
    创建snippet
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    项目参考：paas-ci-backend/VersionInstanceView:30+Jo
    1、类似于Django-CBV写法，在视图类中自行实现各种http请求方法
    2、路由需要自己添加VersionInstanceView.as_view({'get': 'get'})
    3、使用到DRF的Serializer/Response/request.data
    4、校验逻辑全部写入到了请求方法中
    结论：优势在于抽象程度低，便于调试，其次可以充分利用Python类多重继承，将各类公用代码抽离到Mixin类中，
    可以实现代码复用、统一接口返回格式等。最终效果无非就是将特定名称的视图函数比如get_application_list
    归档到某个具体的类的某个请求方法中，比如ApplicationView.get；并且从参考项目中发现，Serializer并未
    完全覆盖参数校验逻辑？
    """

    def _get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self._get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self._get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        # 参数校验
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self._get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===============================================GenericAPIView+Mixin========================================

class SnippetHighlight(generics.GenericAPIView):
    """
    GenericAPIView继承了APIView，是对视图操作中的公共环节，做了进一步的抽象，比如：
    查询model得到数据集：get_queryset
    通过url中的参数获取指定的model对象：get_object
    利用全局过滤类对queryset进行过滤：filter_queryset
    获取序列化类：get_serializer_class
    ...
    通过结合DRF自带的CRUD-mixin，可以比较方便的实现model本身的增删改查
    CRUD-mixin提供了通用的action：create/list/retrieve/update/destroy，
    但是需要使用者将action绑定到具体的http请求方法中，比如在get请求中
    调用ListModeMixin提供的list方法可以快速实现一个带分页功能的数据列表接口
    """
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# 自定义写法：列表+新增
class SnippetList1(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    # 默认返回全部数据，这个不满足常见的场景
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # 可以利用django_filter对url参数进行过滤
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_class = SnippetFilter
    # filter_fields = ('language', )
    filter_fields = {
        'language': ['exact', 'contains'],
        'id': ['gt', 'lt'],
        'owner__username': ['exact'],
    }
    search_fields = ('title', 'code')

    # def get_queryset(self):
    #     """
    #     自定义数据过滤方法，利用url路径参数owner属性过滤数据
    #     利用url查询参数过滤语言
    #     """
    #     owner = self.kwargs['owner']
    #     queryset = Snippet.objects.filter(owner_id=owner)
    #     language = self.request.query_params.get('language', None)
    #     if language is not None:
    #         queryset = queryset.filter(language=language)
    #     return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # 执行保存动作前
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# 简便写法：列表+新增
class SnippetList2(generics.ListCreateAPIView):
    """
    SnippetList2等价于SnippetList1的实现方式（事实上就是这么混入实现的）
    直接使用绑定了http请求方法的视图类：generics.XXXAPIView
    有点在于节省了拼装的成本，通过直接继承常用的几种类图，快速实现常规CURD接口
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer1
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# 自定义写法：查询+更新+删除
class SnippetDetail1(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# 简便写法：查询+更新+删除
class SnippetDetail2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
