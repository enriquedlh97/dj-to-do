from django.db.models.base import ModelBase
from django.views.generic.list import ListView

from .models import Task


class TaskList(ListView):
    model: ModelBase = Task
    context_object_name: str = "tasks"
