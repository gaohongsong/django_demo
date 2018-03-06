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
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views_fbv

# 手动自定义路由
urlpatterns = format_suffix_patterns([
    url(r'^snippets/$', views_fbv.snippet_list, name='snippet-fbv'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views_fbv.snippet_detail, name='snippet-fbv'),
])
