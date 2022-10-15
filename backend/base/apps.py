from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "base"
