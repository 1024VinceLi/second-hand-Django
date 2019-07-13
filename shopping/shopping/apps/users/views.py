from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from users.serializers import SKUSerializer

from goods.models import SKU
from users import serializers, constants
from users.models import User
from users.serializers import AddUserBrowsingHistorySerializer


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
    serializer_class = serializers.EmailSerializer
    permission_classes = [IsAuthenticated]


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


class AddressViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
    用户地址新增与修改
    """
    serializer_class = serializers.UserAddressSerializer
    permissions = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data,
        })

    def create(self, request, *args, **kwargs):
        """
        保存用户地址数据
        """
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message': '保存地址数据已达到上限'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def status(self, request, pk=None, address_id=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True)
    def title(self, request, pk=None, address_id=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = serializers.AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




class UserBrowsingHistoryView(CreateModelMixin, GenericAPIView):
    """
    用户浏览历史记录
    """
    serializer_class = AddUserBrowsingHistorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        保存
        """
        return self.create(request)

    def get(self, request):
        """
        获取
        """
        user_id = request.user.id

        redis_conn = get_redis_connection("history")
        history = redis_conn.lrange("history_%s" % user_id, 0, constants.USER_BROWSING_HISTORY_COUNTS_LIMIT - 1)
        skus = []
        # 为了保持查询出的顺序与用户的浏览历史保存顺序一致
        for sku_id in history:
            sku = SKU.objects.get(id=sku_id)
            skus.append(sku)

        s = SKUSerializer(skus, many=True)
        return Response(s.data)