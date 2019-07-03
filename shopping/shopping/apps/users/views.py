from django.shortcuts import render

# Create your views here.

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

from users import serializers


class UserView(CreateModelMixin, GenericAPIView):
    """
    用户注册
    传入参数
    """
    serializer_class = serializers.CreateUserSerializer

    def post(self):
        # 接受参数

        # 校验参数

        # 保存用户数据

        # 序列化,返回数据
        pass