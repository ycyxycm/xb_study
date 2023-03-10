"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os.path
from pathlib import Path
import logging

from conf.config import *
from conf.exts import *


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tv2*3dr69#0gwz0q_3%st129xh8tw5)z94@cv!8pz3-yjj=fz@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG

ALLOWED_HOSTS = ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',#注册跨域处理
    'rest_framework',#注册rest
    'app.apps.AppConfig',#注册app
    'erp_app.apps.ErpAppConfig',#注册erp_app
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',#跨域处理
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.login_middleware.login_midd',
    'app.middleware.test_middleware.testMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True#允许所有域名跨域(优先选择)

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}
# from logging.handlers import TimedRotatingFileHandler
#配置日志
LOGS_DIR=os.path.join(BASE_DIR,"logs")
if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,# 禁用已经存在的logger实例
    'formatters': {#日志格式器 配置
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'   # 输出格式
        },
        'standard':{
            'format':'%(asctime)s %(levelname)s     %(message)s'
        }
    },
    # 'filters':{#过滤器 配置
    #     'test':{#过滤器名
    #         '()':'ops.TestFilter'#过滤器位置
    #     }
    # },
    'handlers': {#处理器配置
        'console_handler':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'standard'
        },
        'fd_file':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename':os.path.join(LOGS_DIR,f'FD-{get_now_date()}.log'),
            'backupCount': 5,  # 保存备份文件的数量
            'when':'D',
            'interval':1,
            'formatter':'standard',
            'encoding':'utf-8'#文件编码
        },
        'api_file':{
            'level':'INFO',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename':os.path.join(LOGS_DIR,f'API-{get_now_date()}.log'),
            'backupCount': 5,  # 保存备份文件的数量
            'when':'D',
            'interval':1,
            'formatter':'standard',
            'encoding':'utf-8'#文件编码
        },
        'err_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, f'ERR-{get_now_date()}.log'),
            'backupCount': 5,  # 保存备份文件的数量
            'when': 'D',
            'interval': 1,
            'formatter': 'standard',
            'encoding': 'utf-8'  # 文件编码
        },
        'sql_err_file':{
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, f'SQLERR.log'),
            'maxBytes': 1024*1024*300,  # 300 MB
            'backupCount': 5,  # 保存备份文件的数量
            'formatter': 'standard',
            'encoding': 'utf-8'  # 文件编码
        },
        'sql_info_file':{
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, f'SQL.log'),
            'maxBytes': 1024*1024*300,  # 300 MB
            'backupCount': 5,  # 保存备份文件的数量
            'formatter': 'standard',
            'encoding': 'utf-8'  # 文件编码
        },
        'err_simple_file':{
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, f'simpleERR.log'),
            'maxBytes': 1024*1024*300,  # 300 MB
            'backupCount': 5,  # 保存备份文件的数量
            'formatter': 'standard',
            'encoding': 'utf-8'  # 文件编码
        }
        ,
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard'
        },
    },
    'loggers': {
        'fd_log':{
            'handlers':['fd_file'],
            'level':'DEBUG',
            'propagate': False,
        },
        'api_log':{
            'handlers':['api_file','err_file'],
            'level':'INFO',
            'propagate': False,
        },
        'sql_log':{
            'handlers':['sql_info_file','sql_err_file','console_handler'],
            'level':'INFO',
            'propagate': False,
        },
        'err_log':{
            'handlers':['err_simple_file','console_handler'],
            'level':'ERROR',
            'propagate': False,
        }
    },
}

#配置session存储位置
CACHES = {
    "default": { # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL_DEFAULT,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        }
    },
    "session": { # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL_SESSION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        }
    },

    "verify_code": { # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL_VCODE,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        }
    }
}

#配置django-rest 三种认证方式
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',  # token认证
    )
}



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
MEDIA_URL='/media/'
PUB_DIR=Path(__file__).resolve().parent.parent
MEDIA_ROOT=os.path.join(PUB_DIR,'media')

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'		# 上面 CACHES 中设置的名称

CORS_ALLOW_CREDENTIALS = True#设置settings允许携带cookie




