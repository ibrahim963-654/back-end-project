# config/settings.py

from pathlib import Path
from datetime import timedelta
import os                           
from celery.schedules import crontab
from decouple import config


CELERY_BEAT_SCHEDULE = {
    "daily-backup": {
        "task": "core.tasks.daily_backup_task",
        "schedule": crontab(
            hour=0,
            minute=0
        )
    },
    "weekly-reward": {
        "task": "core.tasks.weekly_reward_notification_task",
        "schedule": crontab(
            day_of_week="sun",
            hour=23,
            minute=59
        )
    }
}

# ==========================
# BASE DIR
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================
# SECURITY
# ==========================

SECRET_KEY = "django-project-secret-key-2026-long-random-string"

DEBUG = True

ALLOWED_HOSTS = ['*']


# ==========================
# APPLICATIONS
# ==========================

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third party
    "corsheaders",
    "rest_framework",

    # Your apps
    "core.apps.CoreConfig",
]


# ==========================
# MIDDLEWARE
# ==========================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================
# URL
# ==========================

ROOT_URLCONF = "config.urls"


# ==========================
# TEMPLATES
# ==========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# ==========================
# DATABASE
# ==========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# ==========================
# CUSTOM USER MODEL
# ==========================

AUTH_USER_MODEL = "core.User"


# ==========================
# PASSWORD VALIDATION
# ==========================

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


# ==========================
# REST FRAMEWORK
# ==========================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "core.pagination.CustomPagination",
    "PAGE_SIZE": 20,
}


# ==========================
# JWT SETTINGS
# ==========================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ALGORITHM": "HS256",
}


# ==========================
# CORS
# ==========================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True


# ==========================
# MEDIA FILES
# ==========================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==========================
# STATIC FILES
# ==========================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# ==========================
# LANGUAGE
# ==========================

LANGUAGE_CODE = "ar"
TIME_ZONE = "Africa/Cairo"
USE_I18N = True
USE_TZ = True


# ==========================
# DEFAULT PRIMARY KEY
# ==========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==========================
# EMAIL (FOR PASSWORD RESET)
# ==========================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-password"


# ==========================
# CELERY (BACKUP TASKS)
# ==========================

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"


# ==========================
# FILE UPLOAD
# ==========================

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
