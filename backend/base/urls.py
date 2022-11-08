from django.contrib.auth.views import LogoutView
from django.urls import URLPattern, path

from .views import (
    CustomLoginView,
    TaskCreate,
    TaskDelete,
    TaskDetail,
    TaskList,
    TaskUpdate,
)

urlpatterns: list[URLPattern] = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("", TaskList.as_view(), name="tasks"),
    # The view here looks for a primary key referencing a specific task.
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("task-create/", TaskCreate.as_view(), name="task-create"),
    path("task-update/<int:pk>/", TaskUpdate.as_view(), name="task-update"),
    path("task-delete/<int:pk>/", TaskDelete.as_view(), name="task-delete"),
]
