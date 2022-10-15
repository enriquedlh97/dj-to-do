from django.core.handlers.wsgi import WSGIRequest  # type:ignore
from django.http import HttpResponse  # type: ignore


def task_list(request: WSGIRequest) -> HttpResponse:
    return HttpResponse("To Do List")
