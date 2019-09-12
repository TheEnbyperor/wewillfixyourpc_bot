"""
Django settings for wewillfixyourpc_bot project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, "secrets/SECRET_KEY")) as f:
    SECRET_KEY = f.read()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'mozilla_django_oidc',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'djsingleton',
    'phonenumber_field',
    'fulfillment',
    'facebook',
    'twitter',
    'telegram_bot',
    'azure_bot',
    'operator_interface',
    'payment',
    'rasa_api',
    'gactions',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wewillfixyourpc_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'wewillfixyourpc_bot.wsgi.application'
ASGI_APPLICATION = "wewillfixyourpc_bot.routing.application"

AUTHENTICATION_BACKENDS = [
    'operator_interface.oidc.OIDCAB',
]

OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_CLIENT_ID = "bot-server-dev"
OIDC_RP_CLIENT_SECRET = ""
OIDC_RP_SCOPES = "openid email profile address phone"
OIDC_OP_JWKS_ENDPOINT = "https://account.cardifftec.uk/auth/realms/wwfypc/protocol/openid-connect/certs"
OIDC_OP_AUTHORIZATION_ENDPOINT = "https://account.cardifftec.uk/auth/realms/wwfypc/protocol/openid-connect/auth"
OIDC_OP_TOKEN_ENDPOINT = "https://account.cardifftec.uk/auth/realms/wwfypc/protocol/openid-connect/token"
OIDC_OP_USER_ENDPOINT = "https://account.cardifftec.uk/auth/realms/wwfypc/protocol/openid-connect/userinfo"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SENTRY_ENVIRONMENT = "dev"

EXTERNAL_URL_BASE = "https://wewillfixyourpc-bot.eu.ngrok.io"

STATIC_URL = f'{EXTERNAL_URL_BASE}/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = f'{EXTERNAL_URL_BASE}/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PHONENUMBER_DEFAULT_REGION = "GB"

CELERY_RESULT_BACKEND = "redis://localhost"
CELERY_BROKER_URL = "pyamqp://"
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

with open(os.path.join(BASE_DIR, "secrets/facebook.json")) as f:
    facebook_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/twitter.json")) as f:
    twitter_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/telegram.json")) as f:
    telegram_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/worldpay.json")) as f:
    worldpay_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/azure.json")) as f:
    azure_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/masterpass.json")) as f:
    masterpass_conf = json.load(f)
with open(os.path.join(BASE_DIR, 'secrets/gpay-key-test.pem'), 'rb') as f:
    gpay_priv_key_test = f.read()
with open(os.path.join(BASE_DIR, 'secrets/masterpass-test.p12'), 'rb') as f:
    masterpass_test_p12 = f.read()

AZURE_APP_ID = azure_conf["app-id"]
AZURE_APP_PASSWORD = azure_conf["app-password"]

FACEBOOK_VERIFY_TOKEN = facebook_conf["verify_token"]
FACEBOOK_ACCESS_TOKEN = facebook_conf["access_token"]

TWITTER_CONSUMER_KEY = twitter_conf["consumer_key"]
TWITTER_CONSUMER_SECRET = twitter_conf["consumer_secret"]
TWITTER_ACCESS_TOKEN = twitter_conf["access_token"]
TWITTER_ACCESS_TOKEN_SECRET = twitter_conf["access_token_secret"]

TWITTER_ENVNAME = "main"

TELEGRAM_TOKEN = telegram_conf["token"]
TELEGRAM_PAYMENT_TOKEN = telegram_conf["payment_token"]

WORLDPAY_TEST_KEY = worldpay_conf["test_key"]
WORLDPAY_LIVE_KEY = worldpay_conf["live_key"]

MASTERPASS_TEST_KEY = masterpass_conf["test_key"]
MASTERPASS_TEST_KEY_PASS = masterpass_conf["test_key_pass"]
MASTERPASS_TEST_P12_KEY = masterpass_test_p12

GPAY_TEST_PRIVATE_KEYS = [gpay_priv_key_test]

GOOGLE_PROJECT_ID = "we-will-fix-your-pc-c0198"

RASA_HTTP_URL = "http://172.30.0.13:5005"

DEFAULT_PAYMENT_ENVIRONMENT = "T"

ORDER_NOTIFICATION_EMAIL = "q@misell.cymru"
ORDER_NOTIFICATION_FROM = "noreply@noreply.wewillfixyourpc.co.uk"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

with open(os.path.join(BASE_DIR, "secrets/PUSH_PRIV_KEY")) as f:
    PUSH_PRIV_KEY = f.read()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'twitter': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'facebook': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'telegram_bot': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'azure_bot': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'gactions': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'rasa_api': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'fulfillment': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    },
}
