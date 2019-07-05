from django.shortcuts import render

# Create your views here.
#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.utils import OAuthQQ


class QQAuthURLView(APIView):
    """
    获取QQ登录的url
    """

    def get(self,request):
        """
        提供用于QQ登录的url
        :param request:
        :return:
        """
        next = request.query_params.get('next')
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_qq_login_url()

        return Response({'login_url':login_url})