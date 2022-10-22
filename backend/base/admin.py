from django.contrib import admin  # noqa: F401

from .models import Task

admin.site.register(Task)
