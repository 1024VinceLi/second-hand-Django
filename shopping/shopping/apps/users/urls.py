from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from .views import *

urlpatterns = [
    url(r'^users/$', UserView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', MobileCountView.as_view()), # 手机号验证路由
    url(r'^usernames/(?P<username>\w{5,20})/count/$', UsernameCountView.as_view()),  # 用户名验证路由
    url(r'^authorizations/$', obtain_jwt_token),
    url(r'^email/$', EmailView.as_view()),  # 设置邮箱
    url(r'emails/verification/$',VerifyEmailView.as_view()),
]

router = routers.DefaultRouter()
router.register(r'addresses', AddressViewSet, base_name='addresses')

urlpatterns += router.urls