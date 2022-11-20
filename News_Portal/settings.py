"""
Django settings for News_Portal project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from News_Portal.hidden import * #SECRET_KEY_DJANGO # to hid SECRET_KEY

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY_DJANGO

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# the first page after Authentication
LOGIN_REDIRECT_URL = "/news"
# the first page after log out
# LOGOUT_REDIRECT_URL = "/news"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login"

# use this for signals
SITE_URL = "http://127.0.0.1:8000"

# connect `allauth`
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# AUTHENTICATION OPTIONS - customised
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

# AUTHENTICATION OPTIONS
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True # activate the username filed
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VRIFICATION = 'mandatory' #ACCOUNT_EMAIL_VERIFICATION = 'none'
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True #позволит избежать дополнительных действий и активирует аккаунт сразу, как только мы перейдем по ссылке
ACCOUNT_EMAIL_SUBJECT_PREFIX ='' # delete 'example.com' in subject

ADMINS = [
    ('Me', 'viton4ikk@yandex.ru'),
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', ###
    'django.contrib.flatpages', ###
    'fpages', ###
    'news.apps.NewsConfig', #-# instead using 'news' to activate decorators for senders (setting.py)
    'django_filters', #-#
    'accounts', #-#

     # 3 compulsory apps for `allauth`
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # compulsory app for yandex auth
    'allauth.socialaccount.providers.yandex',
    # list of providers - https://django-allauth.readthedocs.io/en/latest/installation.html

    'django_apscheduler', # наш задачник

]
# формат даты, которую будет воспринимать наш задачник (вспоминаем модуль по фильтрам)
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше,
# но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

SITE_ID = 1 ### flatpages

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'News_Portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  ###
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # connect `allauth`
                'django.template.context_processors.request',
            ],
        },
    },
]


WSGI_APPLICATION = 'News_Portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False#True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/' ###

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / 'static']  ###

# add Celery_redis
CELERY_BROKER_URL = CELERY_BROKER_URL_            # указывает на URL брокера сообщений (Redis). По умолчанию он находится на порту 6379.
CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND_    # указывает на хранилище результатов выполнения задач
CELERY_ACCEPT_CONTENT = ['application/json']      # допустимый формат данных
CELERY_TASK_SERIALIZER = 'json'                   # метод сериализации задач.
CELERY_RESULT_SERIALIZER = 'json'                 # метод сериализации результатов.

