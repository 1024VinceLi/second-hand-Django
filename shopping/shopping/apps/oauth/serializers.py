from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.models import OAuthQQUser
from oauth.utils import OAuthQQ
from users.models import User


class OAuthQQUserSerializer(serializers.Serializer):
    """
    QQ登录常见用户序列化器
    """

    access_token = serializers.CharField(label='操作凭证')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')

    class Meta:
        model = User
        fields = ('mobile', 'password', 'sms_code', 'access_token', 'id', 'username', 'token')
        extra_kwargs = {
            'username':{
                'read_only':True
            },
            'password': {
                'write_only':True,
                'min_length':8,
                'max_length':20,
                'error_messages':{
                    'min_length':'仅允许8-20个字符密码',
                    'max_length': '仅允许8-20个字符的密码',
                }

            }
        }

    def validate(self, data):
        # 检验access_token
        access_token = data['access_token']
        openid = OAuthQQ.check_save_user_token(access_token)

        if not openid:
            raise serializers.ValidationError('无效的access_token')

        data['openid'] = openid

        # 检验短信验证码
        mobile = data['mobile']
        sms_code = data['sms_code']
        redis_conn = get_redis_connection('verify_codes')
        real_sms_code = redis_conn.get("sms_%s" % mobile)
        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码错误')

        # 如果用户存在,检测用户密码

        try:
            user = User.objects.get(mobile = mobile)
        except User.DoesNotExist:
            pass
        else:
            password  = data['password']
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
            data['user'] = user
        return data


    def create(self, validated_data):
        user = validated_data.get('user')
        if not user:
            # 用户不存在
            user = User.objects.create_user(
                username=validated_data['mobile'],
                password=validated_data['password'],
                mobile=validated_data['mobile'],
            )

        OAuthQQUser.objects.create(
            openid=validated_data['openid'],
            user=user
        )
        return user