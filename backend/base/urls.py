from django.urls import URLPattern, path

from .views import TaskCreate, TaskDelete, TaskDetail, TaskList, TaskUpdate

urlpatterns: list[URLPattern] = [
    path("", TaskList.as_view(), name="tasks"),
    # The view here looks for a primary key referencing a specific task.
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("task-create/", TaskCreate.as_view(), name="task-create"),
    path("task-update/<int:pk>/", TaskUpdate.as_view(), name="task-update"),
    path("task-delete/<int:pk>/", TaskDelete.as_view(), name="task-delete"),
]
