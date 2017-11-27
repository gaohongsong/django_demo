"""just_rest_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views


# urlpatterns = [
#     url(r'^$', views.api_root),
#     url(r'^snippets/$', views.SnippetList.as_view()),
#     url(r'^users/$', views.UserList.as_view()),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
#     url(r'users/(?P<pk>\d+)/$', views.UserDetail.as_view())
# ]

# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
# ]

from snippets.views import SnippetViewSet, UserViewSet
# from snippets.views import api_root
from rest_framework import renderers

# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })
#
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy',
# })
#
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
#
# user_list = UserViewSet.as_view({
#     'get': 'list',
# })
#
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve',
# })

from rest_framework.routers import DefaultRouter

# create router and register our viewsets
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

from rest_framework.schemas import SchemaGenerator
# schema_view = SchemaGenerator(title='Miya API')

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^schema/$', schema_view),
]
# urlpatterns = format_suffix_patterns([
#     url(r'^$', api_root),
#     url(r'^snippets/$', snippet_list, name='snippet-list'),
#     url(r'^users/$', user_list, name='user-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
#     url(r'users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
# ])

# urlpatterns = format_suffix_patterns([
#     url(r'^$', views.api_root),
#     url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
#     url(r'^users/$', views.UserList.as_view(), name='user-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(), name='snippet-highlight'),
#     url(r'users/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user-detail')
# ])
