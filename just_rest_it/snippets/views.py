# -*- coding:utf-8 -*-

"""
ViewSetMixin重写了as_view，使其支持通过传入actions_map动态绑定http请求方法，也就是说
请求方法的绑定不再是写死在代码中，而是在实例化ViewSet的时候进行动态绑定

ViewSetMixin + views.APIView = ViewSet

generics.GenericAPIView + ViewSetMixin          => GenericViewSet (带了ViewSetMixin的视图类) +
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin        => ModelViewSet

    # bind actions to http method
    user_list = UserViewSet.as_view({'get': 'list'})
    user_detail = UserViewSet.as_view({'get': 'retrieve'})

    # or register the viewset with a router

    router = DefaultRouter()
    router.register(r'users', UserViewSet, 'user')
    urlpatterns = router.urls

从上面可以看出ModelViewSet区别于ViewSet的地方在于默认混入了
create/list/retrieve/update/delete这些action，即可针对model本身
进行简单的增删改查，若需要进行负载的操作，势必需要重写这些action
或者通过添加新的action，然后利用detail_route绑定到具体的http请求
方法和路由，对外提供接口服务
"""
from django.contrib.auth.models import User

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


class SnippetViewSet(viewsets.ModelViewSet):
    """
    类视图->视图集
    提供了自动注册路由的方法
    抽象程度更高，代码复用性更强，但调试、使用成本更高
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    filter_fields = {
        'language': ['exact', 'contains'],
        'id': ['gt', 'lt'],
        'owner__username': ['exact'],
    }

    # 使用detail_route注册自定义action
    # http://localhost:8000/snippets/1/highlight/
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """内置List/Detail视图"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


# =======================利用viewset生成view函数（确定映射关系）：方法->动作==========================
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
    'get': 'list',
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
})
