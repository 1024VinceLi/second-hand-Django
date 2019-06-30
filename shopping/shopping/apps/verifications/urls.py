from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^image_codes/(?P<image_code_id>[\w-]+/$)',ImageCodeView.as_view()), # 图片验证码路由

]