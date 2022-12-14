from typing import Any, Callable, Literal, Optional, Sequence, Type

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Model
from django.forms import BaseForm, BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormView,
    UpdateView,
)
from django.views.generic.list import ListView

from .models import Task


class CustomLoginView(LoginView):
    """Task Custom Login View: Logs a user in.

    Attributes:
        template_name: Name of the html template to be sued for the login
            form.
        fields: Fields to be shown in the
            form.
        success_url: Function to be used when the
            form is completed.
    """

    template_name: str = "base/login.html"
    fields: Optional[Sequence[str] | Literal["__all__"]] = "__all__"
    redirect_authenticated_user: bool = True

    def get_success_url(self) -> str:
        return reverse_lazy("tasks")


class RegisterPageView(FormView):
    """View for Registering a User.

    Attributes:
        template_name: Name of the html template to be sued for the login
            form.
        form_class: The type of form to use.
        redirect_authenticated_user: Where the user is redirected once the
        form is successfully submitted.
        success_url: Function to be used when the
            form is completed.
    """

    template_name: str = "base/register.html"
    form_class: Optional[Type[BaseForm]] = UserCreationForm
    redirect_authenticated_user: bool = True
    success_url: Optional[str | Callable[..., Any]] = reverse_lazy("tasks")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Creates form for the current user only.

        Args:
            form: Form object for the specific current user.

        Returns:
            HttpResponse to create the form.
        """
        # Makes sure user is logged in
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPageView, self).form_valid(form)

    def get(self, *args, **kwargs) -> HttpResponse:
        """Makes sure authenticated users cannot access register page.

        Returns:
            HttpResponse to redirect to the 'tasks' page or to continue
            registering.
        """
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(RegisterPageView, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    """Task List View: Contains all the tasks displayed.

    By inheriting from 'LoginRequiredMixin', we set a requirement for
    the user to be logged in in order to be able to make modifications.

    Attributes:
        model: Model for the view.
        context_object_name: Name to reference the object within
            the 'task_list.html' template.
    """

    model: Type[Model] = Task
    context_object_name: str = "tasks"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Overwrites method that gets data for the current user only.

        Returns:
            dict[str, Any]: Updated context dict with the user-data only.
        """
        # Inherits context from original object
        context: dict[str, Any] = super().get_context_data(**kwargs)
        # Gets values only for the current user
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        # Defines count of incomplete items
        context["count"] = context["tasks"].filter(complete=False).count()

        search_input: str = self.request.GET.get("search-area") or ""

        if search_input:
            context["tasks"] = context["tasks"].filter(
                title__startswith=search_input
            )

        context["search_input"] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    """Task Detail View: Shows the details for a particular Task.

    Attributes:
        model: Model for the view.
        context_object_name: Name to reference the object within
            the 'task_detail.html' template.
        template_name: Name to use for the template instead of
            'task_detail.html'.
    """

    model: Type[Model] = Task
    context_object_name: Optional[str] = "task"
    template_name: str = "base/task.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    """Task Create View: Creates a Task.

    Attributes:
        model: Model for the view.
        fields: Fields to be shown in the form.
        success_url: Function to be used when the form is completed.
    """

    model: Type[Model] = Task
    # Specifies fields to show in form, this shows all fields from the model
    fields: Optional[Sequence[str] | Literal["__all__"]] = [
        "title",
        "description",
        "complete",
    ]
    # Redirects back to the list of tasks once the new task is created
    success_url: Optional[str | Callable[[str], str]] = reverse_lazy("tasks")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Creates form for the current user only.

        Args:
            form: Form object for the specific current user.

        Returns:
            HttpResponse to create the form.
        """
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """Task Update View: Updates a Task.

    Attributes:
        model (Model): Model for the view.
        fields: Fields to be shown in the
            form.
        success_url: Function to be used when the
            form is completed.
    """

    model: Type[Model] = Task
    # Specifies fields to show in form, this shows all fields from the model
    fields: Optional[Sequence[str] | Literal["__all__"]] = [
        "title",
        "description",
        "complete",
    ]
    # Redirects back to the list of tasks once the new task is created
    success_url: Optional[str | Callable[[str], str]] = reverse_lazy("tasks")


class TaskDelete(LoginRequiredMixin, DeleteView):
    """Task Delete View: Deletes a task.

    Attributes:
        model: Model for the view.
        context_object_name: Name to reference the object within
            the 'task_confirm_delete.html' template.
        success_url: Function to be used when the
            form is completed.
    """

    model: Type[Model] = Task
    context_object_name: str = "task"
    success_url: Optional[str | Callable[[str], str]] = reverse_lazy("tasks")
