import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from shopping.libs.captcha.captcha import captcha
import logging

from shopping.utils.exceptions import logger
from verifications.serializers import ImageCodeCheckSerializer
from shopping.utils.yuntongxun.sms import CCP

from . import constants


class ImageCodeView(APIView):
    """
    图片验证码

    选择APIView的原因:
    不用考虑数据校验,这里也不需要查询数据库
    所以也不需要做序列化操作,不需要序列化器
    """
    def get(self, request, image_code_id):

        # 接受参数
        # 校验参数
        """
        这个两个步骤路由已经帮我们实现了
        """

        # 生成图片验证码
        # text 图片验证码文字
        # image 图片
        text, image = captcha.generate_captcha()

        # 保存真实值
        redis_conn = get_redis_connection("verify_codes")
        # setex 可以保存的时候同时设置有效期
                        # 键           有效期时间     值
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES,text)


        # 返回图片
        print("图片验证码: %s" % text)

        # 因为Response会将内容交给json渲染器进行数据格式转换,所以此处使用HttpResponse
        return HttpResponse(image, content_type="image/jpg")


class SMSCodeView(GenericAPIView):
    '''
    短信验证码
    参入参数:
    mobile image_code_id  text
    '''

    serializer_class = ImageCodeCheckSerializer
    """
    既然继承了GenericAPIView，那为啥不设置queryset属性，只设置了serializer_class属性了呢？
    注意，这里用到谁，就设置谁。
    GenericAPIView没有要求必须都设置的。
    """

    def get(self, request, mobile):
        # 校验参数

        # 获得序列化器
        serializer = self.get_serializer(data = request.query_params)

        # 校验参数
        serializer.is_valid(raise_exception=True)

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0,999999)

        print("短信验证码: %s" % sms_code)

        # 保存短信验证码  发送记录(send_flag)
        redis_conn = get_redis_connection('verify_codes')
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code) # 保存手机号
        # redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1) # 存储发送记录
        # setex(self, name, time, value): (键  过期时间   值)
        """
        1分钟待机时候设置send_flag的原因
        这个逻辑在前端做处理了呀，1分钟倒计时之后才能再次发送短信验证码。是的，但是用户是可以绕过前端，使用postman来发起请求，获取短信验证码的。
        """

        # 使用redis管道
        pl = redis_conn.pipeline() # 创建管道
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        pl.execute() # 放管道通知redis执行命令



        # 发送短信
        try:
            # pass
            # ccp = CCP()
            # expires = constants.SMS_CODE_REDIS_EXPIRES // 60
            # #expires 到期
            #
            # # 发送短信模板
            # result = ccp.send_template_sms(mobile, [sms_code, expires], constants.SMS_CODE_CODE_TEMP_ID)
            result = 0
        except Exception as e:
            logger.error('发送短信验证码[异常]')
            return Response({"message": 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if result == 0:
                # 发送成功

                # 返回
                """
                CCP 返回0 表示发送短信成功
                    返回-1 表示发送失败
                """

                logger.error('发送短信验证码[正常]')
                return Response({"message":'OK'})
            else:
                logger.error('发送短信验证码[失败]')
                return Response({"message":'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



