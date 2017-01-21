# coding=utf-8
"""
Django settings for wzb project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 've#a40)!-a8&obbaj(e^@k0uu%yp(hzpq&s+wm!3fjm_o3+nvw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','192.168.8.179']


# Application definition

INSTALLED_APPS = [
    'wzb',
    'bootstrap3',
    'supplierList',
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stockCode',
    'el_pagination',
    'notifications',
    'keyEvent',
    'payment',


]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.gzip.GZipMiddleware',

]

ROOT_URLCONF = 'wzb.urls'

import os.path

STATIC_ROOT = '/static_all/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join('static'), )

#扩展user字段
# AUTH_USER_MODEL = "wzb.NewUser"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/'],
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

WSGI_APPLICATION = 'wzb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wzb',  # 你的数据库名称
        'USER': 'root',  # 你的数据库用户名
        'PASSWORD': 'root',  # 你的数据库密码
        'HOST': '127.0.0.1',  # 你的数据库主机，留空默认为localhost
        'PORT': '3306',  # 你的数据库端口
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
#TIME_ZONE = 'UTC'
USE_TZ = False
USE_I18N = True

USE_L10N = True

EL_PAGINATION_PER_PAGE=20

#消息通知
NOTIFICATIONS_USE_JSONFIELD=True
NOTIFICATIONS_SOFT_DELETE=True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# STATIC_ROOT = '/public/static '


# STATICFILES_DIRS = (
#     '/static/',
#     )
