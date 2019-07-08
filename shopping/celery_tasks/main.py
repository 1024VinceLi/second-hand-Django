from celery import Celery
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'shopping.settings.dev'


# 创建celery应用
celery_app = Celery("meiduo")

# 导入celery配置
celery_app.config_from_object("celery_tasks.config")

# 导入任务
celery_app.autodiscover_tasks(['celery_task.sms','celery_tasks.email'])