# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework import routers, serializers, viewsets

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')
