from django.core.handlers.wsgi import WSGIHandler
from django.shortcuts import render
from django.urls import path


def index(request):
    return render(request, "index.html")


urlpatterns = [
    path("", index)
]

application = WSGIHandler()
