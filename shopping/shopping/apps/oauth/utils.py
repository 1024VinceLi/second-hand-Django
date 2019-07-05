from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
from django.conf import settings
import json
import logging
from . import constants

logger = logging.getLogger('django')

class OAuthQQ(object):
    """
    QQ认证辅助工具类
    """
    def __init__(self, client_id=None, client_secret=None, redirect_uri = None, state=None):
        self.client_id = client_id or settings.dev.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.dev.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.dev.QQ_REDIRECT_URI
        self.state = state or settings.dev.QQ_STATE


    def get_login_url(self):
        """
        获取qq登录的网址
        :return: url网址
        """
        params = {
            'response_type':'code',
            'client_id':self.client_id,
            'redirect_uri':self.redirect_uri,
            'state':self.state,
            'scope':'get_user_info',
        }
        url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)

        return url