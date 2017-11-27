# -*- coding:utf-8 -*-
"""
https://www.safaribooksonline.com/library/view/lightweight-django/9781491946275/ch04.html
"""

from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework import viewsets, permissions, authentication

from board.serializers import SprintSerializer, UserSerializer, TaskSerializer
from board.models import Sprint, Task


User = get_user_model()


class DefaultsMixin(object):
    """Default settings for view authentication, permission, page, filter"""

    # authentication_classes = (
    #     authentication.BaseAuthentication,
    #     authentication.TokenAuthentication,
    # )
    #
    # permission_classes = (
    #     permissions.IsAuthenticated,
    # )

    paginated_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating sprint"""

    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer


class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating task"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing and creating user"""

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD

    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
