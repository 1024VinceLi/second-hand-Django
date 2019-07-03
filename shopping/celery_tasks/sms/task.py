import logging

from rest_framework.response import Response

# from shopping.utils.exceptions import logger
from celery_tasks.main import celery_app
from shopping.utils.yuntongxun.sms import CCP
from verifications import constants
logger = logging.getLogger('django')

@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, expires, temp_id):
    """
    发送短信验证码
    :return:
    """
    # 发送短信
    try:
        # pass
        # ccp = CCP()
        # expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        # #expires 到期
        #
        # # 发送短信模板
        # result = ccp.send_template_sms(mobile, [sms_code, expires], constants.SMS_CODE_CODE_TEMP_ID)
        result = 0
    except Exception as e:
        logger.error('发送短信验证码[异常]')
        return Response({"message": 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if result == 0:
            # 发送成功

            # 返回
            """
            CCP 返回0 表示发送短信成功
                返回-1 表示发送失败
            """

            logger.error('发送短信验证码[正常]')
            # return Response({"message": 'OK'})
        else:
            logger.error('发送短信验证码[失败]')
            # return Response({"message": 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
