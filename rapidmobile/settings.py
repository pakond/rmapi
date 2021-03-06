"""
Django settings for rapidmobile project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dattfo!5&7-$b!l8b9_g_%$2co!2tj%92(2*f7tpnpqn8yhg^b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.10', '85.49.207.42']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #mis cosas
    'api',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_api_key',
    'corsheaders',
    'django_rest_passwordreset',
    'multiselectfield',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #corsheaders
    'corsheaders.middleware.CorsMiddleware',
    #secure XSS
    'django.middleware.security.SecurityMiddleware',
    #language
    'django.middleware.locale.LocaleMiddleware',
]
SECURE_BROWSER_XSS_FILTER = True

ROOT_URLCONF = 'rapidmobile.urls'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

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

WSGI_APPLICATION = 'rapidmobile.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rapidmobile',
        'USER': 'rapidmobile',
        'PASSWORD': 'rapidmobile',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-Us'

# supported languages
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"), # your static/ files folder
]

# MI CONFIGURACION

AUTH_USER_MODEL = 'api.User'

#APPEND_SLASH=False

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #modificar rest-auth/views.py con este permiso
        #modificar rest-auth/register/app_settings.py con este permiso
        #modificar rest-passwordreset/views.py con este permiso
        #ejemplo: permission_classes = (HasAPIKey,)
        "rest_framework_api_key.permissions.HasAPIKey",
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    #modificar rest-auth/views.py con estos throttles
    #modificar rest-auth/register/views.py con estos throttles
    #modificar rest-passwordreset/views.py con estos throttles
    #ejemplo: throttle_scope = 'login'
    'DEFAULT_THROTTLE_RATES': {
        'register': '4/min',
        'login': '4/min',
        'password_reset': '4/day',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

OLD_PASSWORD_FIELD_ENABLED = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

REST_AUTH_SERIALIZERS = { 
    'USER_DETAILS_SERIALIZER':'api.serializers.UserDetailsSerializer',
    'TOKEN_SERIALIZER': 'api.serializers.TokenSerializer',
}

REST_USE_JWT = True

public_key = open('jwtRS256.public.key', 'r')
private_key = open('jwtRS256.private.key', 'r')

import datetime
from datetime import timedelta

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=15),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
    #'JWT_SECRET_KEY': rskey.read(),
    #'JWT_PUBLIC_KEY': public_key.read(),
    #'JWT_PRIVATE_KEY': private_key.read(),
    #'JWT_ALGORITHM': 'RS256',
}

#CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'x-api-key',
]

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

SITE_URL = 'http://127.0.0.1:8080'
#API_URL = 'http://85.49.207.42:8000/'
API_URL = 'http://127.0.0.1:8000/'
SITE_NAME = 'Rapid Mobile'
SITE_FULL_NAME = 'Rapid Mobile App'