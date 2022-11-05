from django.urls import URLPattern, path

from .views import TaskList

urlpatterns: list[URLPattern] = [
    path("", TaskList.as_view(), name="tasks"),
]
