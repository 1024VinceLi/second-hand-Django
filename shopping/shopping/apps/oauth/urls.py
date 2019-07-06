from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r"qq/authorization/$",QQAuthURLView.as_view()),
    url(r'qq/user/$', QQAuthUserView.as_view()),
]