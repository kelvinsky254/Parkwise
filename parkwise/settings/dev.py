from .base import * #noqa
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default":{
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="parkwise"),
        "USER": config("DB_USER", default="parkwise"),
        "PASSWORD": config("DB_PASSWORD", default="parkwise"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}
