from rest_framework import serializers
from django_redis import get_redis_connection

class ImageCodeCheckSerializer(serializers.Serializer):
    """
    图片验证码校验序列化器
    """

    # 使用UUID获得图片验证码编号
    image_code_id = serializers.UUIDField()

    #
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        """
        校验参数
        :param attrs:
        :return:
        """
        image_code_id = attrs['image_code_id']
        text = attrs['text']


        # 查询真是图片验证码
        redis_conn = get_redis_connection(('verify_codes')) # 建立连接
        # 从数据库取出真实的图片验证码
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)

        if not real_image_code_text: # 如果没有取出来,则表示验证码无效
            raise serializers.ValidationError('图片验证码无效')

        # 比较图片验证码
        real_image_code_text = real_image_code_text.decode() # 因为从redis中取出的是byte类型所以要先解码
        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError("图片验证码不正确")

        # 判断是否在60秒内
        mobile = self.context['views'].kwargs['mobile']
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:  # send_flag 是发送记录
            # 如果取出来了,则表示这个手机号在60秒没请求过一次
            raise serializers.ValidationError('请求次数过于频繁')

        return attrs





