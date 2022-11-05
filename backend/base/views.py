from typing import Callable, Literal, Optional, Sequence, Type

from django.db.models import Model
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Task


class TaskList(ListView):
    """Task List View: Contains all the tasks displayed.

    Attributes:
        model (Model): Model for the view.
        context_object_name (str): Name to reference the object within
            the 'task_list.html' template.
    """

    model: Type[Model] = Task
    context_object_name: str = "tasks"


class TaskDetail(DetailView):
    """Task Detail View: Shows the details for a particular Task.

    Attributes:
        model (Model): Model for the view.
        context_object_name (str): Name to reference the object within
            the 'task_detail.html' template.
        template_name (str): Name to use for the template instead of
            'task_detail.html'.
    """

    model: Type[Model] = Task
    content_type: Optional[str] = "task"
    template_name: str = "base/task.html"


class TaskCreate(CreateView):
    """Task Create View: Creates a Task.

    Attributes:
        model (Model): Model for the view.
        fields (`list` of `str` or `literal`): Fields to be shown in the
            form.
        success_url (`str` or `callable`): Function to be used when the
            form is completed.
    """

    model: Type[Model] = Task
    # Specifies fields to show in form, this shows all fields from the model
    fields: Optional[Sequence[str] | Literal["__all__"]] = "__all__"
    # Redirects back to the list of tasks once the new task is created
    success_url: Optional[str | Callable[[str], str]] = reverse_lazy("tasks")
