"""
Django settings for Hutch.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import os.path
from urllib.parse import urlparse

from django.utils.translation import ugettext_lazy as _
from dotenv import load_dotenv

from app import APP_ROOT


# Load .env file
if os.path.exists(os.path.join(APP_ROOT, ".env")):
    load_dotenv(dotenv_path=os.path.join(APP_ROOT, ".env"))
else:
    load_dotenv(dotenv_path=os.path.join(APP_ROOT, ".env.example"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("APP_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("APP_DEBUG_MODE", "false").lower() == "true")

ALLOWED_HOSTS = (
    []
    if (os.getenv("ALLOWED_HOSTS", "") == "")
    else os.getenv("ALLOWED_HOSTS", "").split(",")
)

# Application definition
INSTALLED_APPS = [
    # 'django.contrib.admin',
    # Incase authentication needed
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django_rq",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # App custom middlewares
    "app.middleware.correlation.Correlation",
    "app.middleware.authentication.Authentication",
    "app.middleware.authorization.Authorization",
    "app.middleware.logging.Logging",
    "app.middleware.errors.Errors",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # Support child themes and themes overriding
            APP_ROOT + "/themes/child",
            APP_ROOT + "/themes/" + os.getenv("CURRENT_THEME", "default"),
            APP_ROOT + "/themes/default",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Email Settings
# https://docs.djangoproject.com/en/3.0/topics/email/
if os.getenv("EMAIL_HOST", None) is not None:
    EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")

if os.getenv("EMAIL_PORT", None) is not None:
    EMAIL_PORT = os.getenv("EMAIL_PORT", 25)

if os.getenv("EMAIL_HOST_USER", None) is not None:
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")

if os.getenv("EMAIL_HOST_PASSWORD", None) is not None:
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

if os.getenv("EMAIL_USE_TLS", None) is not None:
    EMAIL_USE_TLS = (
        True if os.getenv("EMAIL_USE_TLS", "false").lower() == "true" else False
    )

if os.getenv("EMAIL_USE_SSL", None) is not None:
    EMAIL_USE_SSL = (
        True if os.getenv("EMAIL_USE_SSL", "false").lower() == "true" else False
    )

if os.getenv("EMAIL_TIMEOUT", None) is not None:
    EMAIL_TIMEOUT = os.getenv("EMAIL_TIMEOUT", None)

if os.getenv("EMAIL_SSL_KEYFILE", None) is not None and os.path.isfile(
    APP_ROOT + os.getenv("EMAIL_SSL_KEYFILE", "")
):
    EMAIL_SSL_KEYFILE = APP_ROOT + os.getenv("EMAIL_SSL_KEYFILE", "")

if os.getenv("EMAIL_SSL_CERTFILE", None) is not None and os.path.isfile(
    APP_ROOT + os.getenv("EMAIL_SSL_CERTFILE", "")
):
    EMAIL_SSL_CERTFILE = APP_ROOT + os.getenv("EMAIL_SSL_CERTFILE", "")

if os.getenv("EMAIL_BACKEND", None) is not None and os.getenv(
    "EMAIL_BACKEND", None
) in ["smtp", "console", "filebased"]:
    EMAIL_BACKEND = (
        "django.core.mail.backends."
        + os.getenv("EMAIL_BACKEND", "smtp")
        + ".EmailBackend"
    )
    if os.getenv("EMAIL_BACKEND", None) == "filebased":
        EMAIL_FILE_PATH = APP_ROOT + "/storage/mails"


WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
db_connection = os.getenv("DB_CONNECTION")
db_name = os.getenv("DB_DATABASE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

if os.getenv("DATABASE_URL", "") != "":
    url_parts = urlparse(os.getenv("DATABASE_URL", ""))
    db_connection = url_parts.scheme
    db_name = url_parts.path.lstrip("/")
    db_username = url_parts.username
    db_password = url_parts.password
    db_host = url_parts.hostname
    db_port = url_parts.port

if db_connection == "mysql":
    default_db = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": db_name,
        "USER": db_username,
        "PASSWORD": db_password,
        "HOST": db_host,
        "PORT": db_port,
    }
else:
    default_db = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(APP_ROOT + "/storage/database/", "db.sqlite3"),
    }

DATABASES = {"default": default_db}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Logging
# https://docs.djangoproject.com/en/3.0/topics/logging/
DJANGO_LOGGING_HANDLERS = (
    []
    if os.getenv("DJANGO_LOGGING_HANDLERS", "") == ""
    else os.getenv("DJANGO_LOGGING_HANDLERS", "").split(",")
)
DJANGO_LOGGING_LEVEL = (
    "WARNING"
    if os.getenv("DJANGO_LOGGING_LEVEL", "") == ""
    else os.getenv("DJANGO_LOGGING_LEVEL", "").upper()
)
DJANGO_LOGGING_PROPAGATE = (
    True
    if os.getenv("DJANGO_LOGGING_PROPAGATE", "") == ""
    or os.getenv("DJANGO_LOGGING_PROPAGATE", "") == "true"
    else False
)

APP_LOGGING_HANDLERS = (
    ["file"]
    if os.getenv("APP_LOGGING_HANDLERS", "") == ""
    else os.getenv("APP_LOGGING_HANDLERS", "").split(",")
)
APP_LOGGING_LEVEL = (
    "WARNING"
    if os.getenv("APP_LOGGING_LEVEL", "") == ""
    else os.getenv("APP_LOGGING_LEVEL", "").upper()
)
APP_LOGGING_PROPAGATE = (
    True
    if os.getenv("APP_LOGGING_PROPAGATE", "") == ""
    or os.getenv("APP_LOGGING_PROPAGATE", "").lower() == "true"
    else False
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(filename)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {
            "format": "%(levelname)s %(asctime)s %(message)s {'correlationId':'%(correlation_id)s'}"
        },
    },
    "filters": {
        "correlation_filter": {
            "()": "app.middleware.correlation.CorrelationFilter",
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "filters": ["correlation_filter"],
            "class": "logging.FileHandler",
            "filename": os.path.join(
                APP_ROOT + "/storage/logs/", "dev" if DEBUG else "prod" + ".log"
            ),
            "formatter": "simple",
        },
        "console": {
            "level": "DEBUG",
            "filters": ["correlation_filter"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": DJANGO_LOGGING_HANDLERS,
            "level": DJANGO_LOGGING_LEVEL,
            "propagate": DJANGO_LOGGING_PROPAGATE,
        },
        "app": {
            "handlers": APP_LOGGING_HANDLERS,
            "level": APP_LOGGING_LEVEL,
            "propagate": APP_LOGGING_PROPAGATE,
        },
        "django.db.backends": {
            "handlers": APP_LOGGING_HANDLERS,
            "level": APP_LOGGING_LEVEL,
            "propagate": APP_LOGGING_PROPAGATE,
        },
        "django.request": {
            "handlers": APP_LOGGING_HANDLERS,
            "level": APP_LOGGING_LEVEL,
            "propagate": APP_LOGGING_PROPAGATE,
        },
        "django.server": {
            "handlers": APP_LOGGING_HANDLERS,
            "level": APP_LOGGING_LEVEL,
            "propagate": APP_LOGGING_PROPAGATE,
        },
        "django.template": {
            "handlers": APP_LOGGING_HANDLERS,
            "level": APP_LOGGING_LEVEL,
            "propagate": APP_LOGGING_PROPAGATE,
        },
    },
}

CSRF_FAILURE_VIEW = "app.controllers.web.error.csrf_failure"

# Languages List
LANGUAGES = (("fr", _("French")), ("en", _("English")), ("de", _("Deutsch")))

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv("APP_TIMEZONE", "UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = ["app.backend.api_key.ApiKeyBackend"]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"

STATIC_ROOT = APP_ROOT + STATIC_URL

STATICFILES_DIRS = [APP_ROOT + "/assets"]

LOCALE_PATHS = [APP_ROOT + "/translation/"]

# RQ Queue Configs
RQ_QUEUES = {
    "default": {
        "HOST": os.getenv("REDIS_HOST"),
        "PORT": int(os.getenv("REDIS_PORT")),
        "DB": int(os.getenv("REDIS_DB")),
        "PASSWORD": os.getenv("REDIS_PASSWORD"),
        "DEFAULT_TIMEOUT": 360,
    }
}
