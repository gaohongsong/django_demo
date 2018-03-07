# -*- coding: utf-8 -*-

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

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import SchemaGenerator

from snippets import views

# 注册viewsets到路由
router = DefaultRouter(trailing_slash=True)

router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

schema_view = SchemaGenerator(title='Miya API')

# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^schema/$', schema_view),
# ]

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/highlight/(?P<pk>[0-9]+)/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'^users/$', views.user_list),
    url(r'^users/(?P<pk>[0-9]+)/$', views.snippet_detail),
]