from celery import Celery

# 创建celery应用
celery_app = Celery("meiduo")

# 导入celery配置
celery_app.config_from_object("celery_tasks.config")

# 导入任务
celery_app.autodiscover_tasks(['celery_task.sms'])