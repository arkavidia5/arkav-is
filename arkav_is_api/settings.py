"""
Django settings for arkav_is_api project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import dj_database_url
import nested_admin
from distutils.util import strtobool

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'nested_admin',
    'arkav_is_api.arkavauth',
    'arkav_is_api.uploader',
    'arkav_is_api.competition',
    'arkav_is_api.preevent',
    'arkav_is_api.quiz',
    'arkav_is_api.seminar',
]
AUTH_USER_MODEL = 'arkavauth.User'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'arkav_is_api.urls'

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

WSGI_APPLICATION = 'arkav_is_api.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}


# -----------------------------
# ENVIRONMENT-SPECIFIC SETTINGS
# -----------------------------


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv('DEBUG', 'False'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'z4z#u2gmm(+3^!$7b^kc3ijq8p3o&&hekk#^7er2o5)!3e*rp9')

ALLOWED_HOSTS = [
    'dashboard.arkavidia.id',
    'arkavidia.id',
    'localhost',
]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# Read from DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.config(default="sqlite:///" + os.path.join(BASE_DIR, 'db.sqlite3')),
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Jakarta')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(BASE_DIR, 'static/'))

# File uploads will be stored in this directory

MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, 'uploads/'))

# Email settings

EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
EMAIL_PORT = os.getenv('EMAIL_PORT', '587')
EMAIL_USE_TLS = strtobool(os.getenv('EMAIL_USE_TLS', 'True'))

DEFAULT_FROM_EMAIL = 'Arkavidia 5.0 <noreply@arkavidia.id>'
CODING_CLASS_REGISTRATION_OPEN = strtobool(os.getenv('CODING_CLASS_REGISTRATION_OPEN', 'False'))
# Security-related settings - only enable if HTTPS is enabled

CSRF_COOKIE_SECURE = strtobool(os.getenv('CSRF_COOKIE_SECURE', 'False'))
SESSION_COOKIE_SECURE = strtobool(os.getenv('SESSION_COOKIE_SECURE', 'False'))
