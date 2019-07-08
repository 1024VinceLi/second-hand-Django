"""
Django settings for shopping project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
# print(sys.path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e&c2x^9t7)q)gt0ukne91*g=-^jwtj41n=edo_0h@-^kp$r%&u'




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True












# jango发送邮件配置信息
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
#发送邮件的邮箱
EMAIL_HOST_USER = 'itcast88@163.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'python808'
#收件人看到的发件人
EMAIL_FROM = 'python<itcast88@163.com>'






















# 配置前后端域名
ALLOWED_HOSTS = ["127.0.0.1", 'www.meiduo.site', 'api.meiduo.site', 'localhost']








# QQ登录参数配置
QQ_CLIENT_ID = '101474184'
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
QQ_STATE = '/'












# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    # 'shopping.apps.users.apps.UsersConfig' # 注册应用
    'users.apps.UsersConfig', # 注册应用
    'verifications.apps.VerificationsConfig',  # 注册图片验证码子应用
    'corsheaders', # 处理跨域请求第三方件
    'oauth.apps.OauthConfig',
]










MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]




ROOT_URLCONF = 'shopping.urls'





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]








WSGI_APPLICATION = 'shopping.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }







# mysql数据库配置信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'meiduo',  # 数据库用户名
        'PASSWORD': 'meiduo',  # 数据库用户密码
        'NAME': 'meiduo'  # 数据库名字
    }
}


# redis数据库配置信息
CACHES = {
    "default": {  # 默认信息存储
        "BACKEND": "django_redis.cache.RedisCache",  # 存储到redis缓存中
        "LOCATION": "redis://127.0.0.1:6379/0",   # 0号仓库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session信息存储
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # 1号仓库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_codes": {  # 图片验证码存储
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",   # 2号仓库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}







# 给adim站点使用
SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # cache 缓存
SESSION_CACHE_ALIAS = "session"















# CORS设置白名单
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    'localhost:8080',
    'www.meiduo.site:8080',
    'api.meiduo.site:8000',
)





CORS_ALLOW_CREDENTIALS = True # 允许携带cookie


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/











# 设置日志

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],
            'propagate': True,
        },
    }
}


REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'shopping.utils.exceptions.exception_handler',
    # "DEFAULT_RENDERER_CLASSES":(  # 默认响应渲染类
    #     'rest_framework.renderers.JSONRenderer',  # json渲染器
    #     'rest_framework.renderers.BrowsableAPIRenderer'  # 浏览API渲染器
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {  # JWT配置 token有效期为1天
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}


AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend'
]

# 注册模型类
AUTH_USER_MODEL = "users.User"



# 语言设置
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai' # 设置时区

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
