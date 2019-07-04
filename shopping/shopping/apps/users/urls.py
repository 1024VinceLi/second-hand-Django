from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^users/$', UserView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view()), # 手机号验证路由
    url(r'^usernames/(?P<username>\w{5,20})/count/$', UsernameCountView.as_view()),  # 用户名验证路由
]