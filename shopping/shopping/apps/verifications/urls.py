from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^image_codes/(?P<image_code_id>[\w-]+)/$",ImageCodeView.as_view()), # 图片验证码路由
    url(r'^sms_code/(?P<mobile>1[3-9]\d{9})/$',SMSCodeView.as_view())

]