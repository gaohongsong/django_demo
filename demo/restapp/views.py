# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from restapp.models import Profile
from restapp.serializers import UserSerializer, ProfileSerializer
from restapp.serializers import UserSerializer1


class UserViewSet(viewsets.ViewSet):
    """
    普通类视图
    """

    def list(self, request):
        users = User.objects.all()
        serialzer = UserSerializer(users, many=True)
        return Response(serialzer.data)

    def fetch(self, request, pk=None):
        users = User.objects.all()
        user = get_object_or_404(users, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# 从类视图转换到函数视图
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'fetch'})


class ProfileViewSet(viewsets.ModelViewSet):
    """Model视图"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
