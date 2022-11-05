from django.urls import URLPattern, path

from .views import TaskCreate, TaskDetail, TaskList

urlpatterns: list[URLPattern] = [
    path("", TaskList.as_view(), name="tasks"),
    # The view here looks for a primary key referencing a specific task.
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("task-create/", TaskCreate.as_view(), name="task-create"),
]
