# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib.auth import views
from django.views.generic import TemplateView

from auth.forms import LoginForm

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}),
    # url(r'^login/$', views.login, {'template_name': 'login_basic.html', 'authentication_form': LoginForm}),
    url(r'^logout/$', views.logout, {'template_name': 'logout.html'})
    # url(r'^logout/$', views.logout, {'next_page': '/login/'})
]
