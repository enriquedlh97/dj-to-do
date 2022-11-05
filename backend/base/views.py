from django.db.models.base import ModelBase
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Task


class TaskList(ListView):
    """Task List View: Contains all the tasks displayed.

    Attributes:
        model (ModelBase): Model for the view.
        context_object_name (str): Name to reference the object within
            the 'task_list.html' template.
    """

    model: ModelBase = Task
    context_object_name: str = "tasks"


class TaskDetail(DetailView):
    """Task Detail View: Shows the details for a particular Task.

    Attributes:
        model (ModelBase): Model for the view.
        context_object_name (str): Name to reference the object within
            the 'task_detail.html' template.
        template_name (str): Name to use for the template instead of
            'task_detail.html'.
    """

    model: ModelBase = Task
    context_object_name: str = "task"
    template_name: str = "base/task.html"
