from django.core.handlers.wsgi import WSGIHandler
from django.urls import path
from django.views.generic import TemplateView
from github_api import GithubApi


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        repos_list = ['bookishop', 'webbinspace']
        bumps, bumps_status = self.fetch_bumps(repos_list)
        context['bumps'] = bumps
        context['bumps_status'] = bumps_status
        return context

    def fetch_bumps(self, repos_list):
        """
        Fetch pull requests for each repository in the given list
        and extract dependency bumps.

        This method processes each repository, retrieves its pull requests,
        and identifies dependency bump updates made by Dependabot. It returns
        a list of bump dictionaries and a status string indicating the overall
        result.

        :param repos_list: A list of repository names to process
        :return: A tuple containing:
            - bumps (list): A list of dictionaries, each representing a dependency bump
            - bumps_status (str): A status string ('success', 'warning', or 'danger')
              corresponding to Bootstrap color classes for green, yellow, and red,
              respectively
        """
        gh = GithubApi()
        bumps = []
        bumps_status = 'success'

        for reponame in repos_list:
            pulls = gh.get_repo_pulls('marketulinek', reponame)
            if pulls is not None:
                dependabot_pulls = filter(self.is_dependabot_bump, pulls)
                bumps.extend(self.process_pulls(dependabot_pulls, reponame))

        if len(bumps) > 0:
            bumps_status = 'warning'

        return bumps, bumps_status

    def process_pulls(self, pulls, reponame):
        """
        Process the list of pull requests for a single repository.
        Filter out the relevant dependabot bumps and extracts updates.

        :param pulls: A list of dictionaries, each representing a pull request
        :param reponame: A repository name
        :return: A list of dictionaries, each representing a dependency bump
        """
        bumps = []
        for pull in pulls:
            updates = self.extract_dependency_bump(pull)
            for update in updates:
                new_bump = self.parse_bump(update, reponame)
                bumps.append(new_bump)
        return bumps

    @staticmethod
    def is_dependabot_bump(pull):
        """
        Check if a pull request is dependabot bump.

        :param pull: A pull request
        :return: True if the pull request is dependabot bump, False otherwise
        """
        return pull['user']['login'] == 'dependabot[bot]' and pull['title'].startswith('Bump ')

    @staticmethod
    def extract_dependency_bump(pull):
        """
        Extract dependency bump details from a dependabot pull request.

        This method checks if the bump is for a single library or a bundle of libraries
        and extracts the relevant update information.

        :param pull: Pull request data
        :return: List of update titles
        """
        if 'Bump the bundler group' in pull['title']:
            content_lines = pull['body'].split('\n')
            return [line.replace('`', '') for line in content_lines if line.startswith('Updates `')]
        else:
            return [pull['title']]

    @staticmethod
    def parse_bump(update, reponame):
        title_parts = update.split()
        return {
            'reponame': reponame,
            'library': title_parts[1],
            'from': title_parts[3],
            'to': title_parts[5],
        }


urlpatterns = [
    path("", IndexView.as_view(), name='index'),
]

application = WSGIHandler()
