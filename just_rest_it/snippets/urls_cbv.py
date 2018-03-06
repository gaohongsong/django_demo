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

from snippets import views_cbv

# 手动自定义路由
urlpatterns = format_suffix_patterns([
    url(r'^users/$', views_cbv.UserList.as_view()),
    url(r'users/(?P<pk>\d+)/$', views_cbv.UserDetail.as_view()),

    url(r'^snippets/$', views_cbv.SnippetList.as_view(), name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views_cbv.SnippetDetail.as_view(), name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views_cbv.SnippetHighlight.as_view()),

    url(r'^snippets1/$', views_cbv.SnippetList1.as_view(), name='snippet-list'),
    url(r'^snippets1/(?P<pk>[0-9]+)/$', views_cbv.SnippetDetail1.as_view(), name='snippet-detail'),
])
