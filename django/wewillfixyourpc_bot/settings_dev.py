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
    "django.contrib.admin",
    "django.contrib.auth",
    "django_keycloak_auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "djsingleton",
    "phonenumber_field",
    "fulfillment",
    "facebook",
    "twitter",
    "telegram_bot",
    "azure_bot",
    "operator_interface",
    "customer_chat",
    "rasa_api",
    "api",
    "gactions",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_keycloak_auth.middleware.OIDCMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "wewillfixyourpc_bot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "wewillfixyourpc_bot.wsgi.application"
ASGI_APPLICATION = "wewillfixyourpc_bot.routing.application"

AUTHENTICATION_BACKENDS = ["django_keycloak_auth.auth.KeycloakAuthorization"]

LOGIN_URL = "oidc_login"
LOGOUT_REDIRECT_URL = "oidc_login"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "OPTIONS": {"timeout": 20},
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("localhost", 6379)]},
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


SENTRY_ENVIRONMENT = "dev"

EXTERNAL_URL_BASE = "https://wewillfixyourpc-bot.eu.ngrok.io"

STATIC_URL = f"{EXTERNAL_URL_BASE}/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = f"{EXTERNAL_URL_BASE}/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

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
with open(os.path.join(BASE_DIR, "secrets/azure.json")) as f:
    azure_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/keycloak.json")) as f:
    keycloak_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/blip.json")) as f:
    blip_conf = json.load(f)

AZURE_APP_ID = azure_conf["app-id"]
AZURE_APP_PASSWORD = azure_conf["app-password"]

FACEBOOK_VERIFY_TOKEN = facebook_conf["verify_token"]
FACEBOOK_ACCESS_TOKEN = facebook_conf["access_token"]
FACEBOOK_APP_SECRET = facebook_conf["app_secret"]
FACEBOOK_OPTIN_SECRET = facebook_conf["optin_secret"]

TWITTER_CONSUMER_KEY = twitter_conf["consumer_key"]
TWITTER_CONSUMER_SECRET = twitter_conf["consumer_secret"]
TWITTER_ACCESS_TOKEN = twitter_conf["access_token"]
TWITTER_ACCESS_TOKEN_SECRET = twitter_conf["access_token_secret"]

TWITTER_ENVNAME = "main"

TELEGRAM_TOKEN = telegram_conf["token"]
TELEGRAM_PAYMENT_TOKEN = telegram_conf["payment_token"]

BLIP_KEY = blip_conf["key"]

GOOGLE_PROJECT_ID = "we-will-fix-your-pc-dev"

RASA_HTTP_URL = "http://172.30.0.13:5005"

DEFAULT_PAYMENT_ENVIRONMENT = "TEST"
PAYMENT_HTTP_URL = "https://wwfypc-payments.eu.ngrok.io"
PAYMENT_EXTERNAL_URL = "https://wwfypc-payments.eu.ngrok.io"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

KEYCLOAK_SERVER_URL = keycloak_conf["server_url"]
KEYCLOAK_REALM = keycloak_conf["realm"]
OIDC_CLIENT_ID = keycloak_conf["client_id"]
OIDC_CLIENT_SECRET = keycloak_conf["client_secret"]
OIDC_SCOPES = keycloak_conf["scopes"]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

with open(os.path.join(BASE_DIR, "secrets/PUSH_PRIV_KEY")) as f:
    PUSH_PRIV_KEY = f.read()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"level": "DEBUG", "filters": None, "class": "logging.StreamHandler"}
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # },
        "twitter": {"handlers": ["console"], "level": "DEBUG"},
        "facebook": {"handlers": ["console"], "level": "DEBUG"},
        "telegram_bot": {"handlers": ["console"], "level": "DEBUG"},
        "azure_bot": {"handlers": ["console"], "level": "DEBUG"},
        "gactions": {"handlers": ["console"], "level": "DEBUG"},
        "rasa_api": {"handlers": ["console"], "level": "DEBUG"},
        "fulfillment": {"handlers": ["console"], "level": "DEBUG"},
        "django_keycloak_auth": {"handlers": ["console"], "level": "DEBUG"},
        "keycloak": {"handlers": ["console"], "level": "DEBUG"},
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
