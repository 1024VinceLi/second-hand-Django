from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer


# Create your models here.
from users import constants


class User(AbstractUser):
    """用户模型类"""
                             # 最大长度为11    唯一,不可重复    昵称为 手机号
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = "tb_users"
        verbose_name = '用户'  # 人性化显示

        verbose_name_plural = verbose_name
        # plural  复数形式

    def generate_verify_email_url(self):
        """
        生成验证邮箱的url
        :return:
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TIKEN_EXPIRES)
        data = {'user_id': self.id, 'email':self.email}
        token= serializer.dumps(data).decode()
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token

        return verify_url