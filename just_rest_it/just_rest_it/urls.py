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
from django.contrib import admin

from rest_framework import routers, serializers, viewsets
from snippets.views import UserViewSet, SnippetViewSet

router = routers.DefaultRouter()
router.register(prefix=r'users', viewset=UserViewSet, base_name='users')
router.register(r'snippets', SnippetViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # 提供rest-api登录入口
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    # 测试cbv写法
    # url(r'^', include('snippets.urls_cbv')),
    # 测试fbv写法
    # url(r'^', include('snippets.urls_fbv')),
]
