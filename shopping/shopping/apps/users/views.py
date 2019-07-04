from django.shortcuts import render

# Create your views here.

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers
from users.models import User


class UserView(CreateAPIView):
    """
    用户注册
    传入参数
    """
    serializer_class = serializers.CreateUserSerializer

    # def post(self):
        # 接受参数

        # 校验参数

        # 保存用户数据

        # 序列化,返回数据
        # pass


class UsernameCountView(APIView):
    """
    用户数量
    """

    def get(self, request, username):
        """
        获取指定用户数量
        :param request:
        :param username:
        :return:
        """

        count = User.objects.filter(username=username).count()

        data = {
            'username' : username,
            'count': count
        }

        return Response(data)


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    手机号数量
    """

    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)

