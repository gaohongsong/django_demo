# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers

from restapp.models import Profile


class UserSerializer(serializers.ModelSerializer):
    """
    继承自ModelSerializer
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'is_superuser')
        # fields = '__all__'

        # select_related
        depth = 1
        # exclude = ('password',)


class UserSerializer1(serializers.Serializer):
    """
    继承自Serializer
    """

    username = serializers.CharField(max_length=125)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'is_superuser')


class ProfileSerializer(serializers.ModelSerializer):
    """
    关联外键处理方式
    """

    # 取外键的某个字段
    username = serializers.CharField(source='user.username', read_only=True)
    # 取model中的方法和property(sex)
    user_detail = serializers.CharField(source='get_absolute_url', read_only=True)
    # 取外键的主键
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    # 取外键的访问地址
    user_url = serializers.HyperlinkedRelatedField(source='user',
                                                   view_name='restapp.views.user_detail',
                                                   queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ('user', 'telephone', 'username', 'user_url', 'user_id', 'user_detail', 'sex')
        depth = 1
