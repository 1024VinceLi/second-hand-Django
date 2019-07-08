from django.shortcuts import render

# Create your views here.
from rest_framework import status

from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
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


# GET /user/
class USerDetailView(RetrieveAPIView):
    """
    用户基本信息
    """
    serializer_class = serializers.UserDetailSerializer

    # queryset = User.objects.all()
    permission_classes = [IsAuthenticated] # 指明必须登陆后才可以访问

    def get_object(self):
        # 返回当前请求的用户

        # 在类视图对象中可以通过类视图对象的属性获取request

        # 在django的请求request对象总,user属性表明当请求的用户
        return self.request.user






class EmailView(UpdateAPIView):
    """
    保存用户邮箱
    """
    permission_classes = [IsAuthenticated]
    serializers_class = serializers.EmailSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user



class VerifyEmailView(APIView):
    """
    邮箱验证
    """
    def get(self, request):
        # 获取token
        token = request.query_params.get('token')

        if not token:
            return Response({'message':'缺少token'},status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        user = User.check_verify_email_token(token)

        if user is None:
            return Response({'message':'链接信息无效'}, status=status.HTTP_400_BAD_REQUEST )
        else:
            user.email_active = True
            user.save()

            return Response({'message':'OK'})














