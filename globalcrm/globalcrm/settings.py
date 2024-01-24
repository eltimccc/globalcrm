import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-hz2xhua15lq6br#s62b!67v&mqcq%dibre0(q$h0n&xt8=d7v1"

DEBUG = os.getenv("DEBUG")


ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "schedule",
    "django.contrib.staticfiles",
    "tasks.apps.TasksConfig",
    "users.apps.UsersConfig",
    "uploads.apps.UploadsConfig",
    "prices",
    "clients",
    "cars",
    "contracts",
    "crispy_forms",
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.services.middleware.LogoutRedirectMiddleware",
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ROOT_URLCONF = "globalcrm.urls"

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
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

WSGI_APPLICATION = "globalcrm.wsgi.application"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"

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

LANGUAGE_CODE = "en-us"
USE_TZ = True
TIME_ZONE = "Europe/Moscow"
DATETIME_FORMAT = "m.d.Y H:i"
DATE_FORMAT = "m.d.Y H:i"
DATE_INPUT_FORMATS = ['%d.%m.%Y %H:%M']

USE_I18N = True

STATIC_ROOT = "staticfiles"
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django crispy forms

# CRISPY_TEMPLATE_PACK = 'bootstrap5'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# end