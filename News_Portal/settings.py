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

import django.utils.log

from News_Portal.hidden import * #SECRET_KEY_DJANGO # to hide a SECRET_KEY

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

    'django_apscheduler', # ?????? ????????????????

]
# ???????????? ????????, ?????????????? ?????????? ???????????????????????? ?????? ???????????????? (???????????????????? ???????????? ???? ????????????????)
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# ???????? ???????????? ???? ?????????????????????? ???? 25 ????????????, ???? ?????? ?????????????????????????? ??????????????????, ???????????? ?????????????????? ?????????? ????????????????,
# ???? ?????? ??????????????, ?????? ???????????? ???????? ???? ???????????????????????????????????? ??????????????
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

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/' ###

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / 'static']  ###

# add Celery_redis

CELERY_BROKER_URL = 'redis://localhost:6379'        # ?????????????????? ???? URL ?????????????? ?????????????????? (Redis - linux version). ???? ?????????????????? ???? ?????????????????? ???? ?????????? 6379.
CELERY_RESULT_BACKEND = 'redis://localhost:6379'    # ?????????????????? ???? ?????????????????? ?????????????????????? ???????????????????? ?????????? (Redis - linux version)

CELERY_ACCEPT_CONTENT = ['application/json']      # ???????????????????? ???????????? ????????????
CELERY_TASK_SERIALIZER = 'json'                   # ?????????? ???????????????????????? ??????????.
CELERY_RESULT_SERIALIZER = 'json'                 # ?????????? ???????????????????????? ??????????????????????.
CELERY_TASK_TIME_LIMIT = 30 * 60                  # time limit for task processing


# cache (files using)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # ??????????????????, ???????? ?????????? ?????????????????? ???????????????????? ??????????! ???? ???????????????? ?????????????? ?????????? cache_files ???????????? ?????????? ?? manage.py!
        'TIMEOUT' : 30,                                   # 300 sec - default, 'none' -never
        'OPTIONS': {
            'MAX_ENTRIES': 200 # ???????????????????????? ???????????????????? ??????????????????, ?????????????????????? ?? ???????? ???? ???????????????? ???????????? ????????????????. ???????? ???????????????? ???????????????????? ???? 300 ??????????????????.
        }
    }
}

# D13.4
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'django': {
            'handlers': ['console_general', 'console_warning', 'console_error', 'general', 'news'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['error', 'mail_admins'],
            'level': 'DEBUG',
        },
        'django.server': {
            'handlers': ['error', 'mail_admins'],
            'level': 'DEBUG',
        },
        'django.template': {
            'handlers': ['error'],
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['error'],
            'level': 'DEBUG',
        },
        'django.security': {
            'handlers': ['security'],
            'level': 'DEBUG',
        },
    },
    'handlers': {
        'console_general': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_general',
            'filters': ['require_debug_true'],
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning',
            'filters': ['require_debug_true'],
        },
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'console_error',
            'filters': ['require_debug_true'],
        },
        'general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'general',
            'filters': ['require_debug_false'],
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'console_error',
        },
        'security': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'general',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'console_warning',
            'filters': ['require_debug_false'],
        },
        'news': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'news',
        },
    },
    'formatters': {
        'console_general': {
            'format': '{levelname} {asctime}: "{message}"',
            'style': '{',
        },
        'console_warning': {
            'format': '{levelname} {asctime}: "{message}" - {pathname}',
            'style': '{',

        },
        'console_error': {
            'format': '{levelname} {asctime}: "{message}" - {pathname} -- {exc_info}',
            'style': '{',

        },
        'general': {
            'format': '{levelname} {asctime}: {module} - "{message}"',
            'style': '{',

        },
        'news': {
            'format': '{levelname} {asctime}: <<{module}>> - "{message}" -- <<{pathname}>>',
            'style': '{',

        },

    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
}

