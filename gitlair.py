from django.core.handlers.wsgi import WSGIHandler
from django.shortcuts import render
from django.urls import path
from github_api import GithubApi


def index(request):
    # Dependabot bumps state
    gh = GithubApi()
    bumps = []
    repos_list = ['bookishop', 'webbinspace']
    for reponame in repos_list:
        pulls = gh.get_repo_pulls('marketulinek', reponame)
        for pull in pulls:
            if pull['user']['login'] == 'dependabot[bot]' and pull['title'][:5] == 'Bump ':

                updates = []
                if 'Bump the bundler group with ' in pull['title']:
                    content_lines = pull['body'].split('\n')
                    for line in content_lines:
                        if line[:9] == 'Updates `':
                            updates.append(line.replace('`', ''))
                else:
                    updates.append(pull['title'])

                for update in updates:
                    title_parts = update.split()
                    new_bump = {
                        'reponame': reponame,
                        'library': title_parts[1],
                        'from': title_parts[3],
                        'to': title_parts[5],
                    }
                    bumps.append(new_bump)
    context = {'bumps': bumps}
    return render(request, "index.html", context)


urlpatterns = [
    path("", index)
]

application = WSGIHandler()
