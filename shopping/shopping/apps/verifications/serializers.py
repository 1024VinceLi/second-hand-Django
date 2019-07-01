from rest_framework import serializers
from django_redis import get_redis_connection

class ImageCodeCheckSerializer(serializers.Serializer):
    """
    图片验证码校验序列化器
    """

    # 使用UUID获得图片验证码编号
    image_code_id = serializers.UUIDField()

    #
    # text =
    pass