from django.core.handlers.wsgi import WSGIHandler
from django.shortcuts import render
from django.urls import path
from github_api import GithubApi


def index(request):
    gh = GithubApi()
    pulls = gh.get_repo_pulls('marketulinek', 'bookishop')
    bumps = []
    for pull in pulls:
        bumps.append(pull)
    return render(request, "index.html")


urlpatterns = [
    path("", index)
]

application = WSGIHandler()
