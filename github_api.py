import requests


class GithubApi:
    """
    A class for interacting with the GitHub API.

    This class provides methods for making GitHub API requests,
    checking rate limits, and retrieving data.
    """
    BASE_URL = 'https://api.github.com/'
    URL_RATE_LIMIT = f'{BASE_URL}rate_limit'
    URL_USER_REPOS = f'{BASE_URL}/users/{{}}/repos'
    URL_REPO = f'{BASE_URL}repos/{{}}'
    URL_REPO_CONTENT = f'{BASE_URL}repos/{{}}/contents'
    URL_REPO_PULLS = f'{BASE_URL}repos/{{}}/{{}}/pulls'

    HEADERS = {'content-type': 'application/json'}

    def request(self, url):
        if not self._rate_limit_ok():
            print("GitHub API rate limit exceeded")
            return None

        response = self._make_api_request(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_user_repos(self, username):
        url = self.URL_USER_REPOS.format(username)
        return self.request(url)

    def get_repo_pulls(self, username, reponame):
        # https://api.github.com/repos/marketulinek/bookishop/pulls
        url = self.URL_REPO_PULLS.format(username, reponame)
        return self.request(url)

    def _make_api_request(self, url):
        """Makes a GET request to the specified URL."""
        return requests.get(url, headers=self.HEADERS)

    def _rate_limit_ok(self):
        """Checks if the GitHub API rate limit is sufficient."""
        try:
            r = self._make_api_request(self.URL_RATE_LIMIT)
            rate_limit = int(r.json()['resources']['core']['remaining'])
            return rate_limit > 0
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while checking GitHub API rate limit: {e}")
            return False



# https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app


# https://blog.apify.com/python-github-api/

# https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api?apiVersion=2022-11-28

# https://docs.github.com/en/rest/dependabot/alerts?apiVersion=2022-11-28#list-dependabot-alerts-for-a-repository
# https://api.github.com/repos/OWNER/REPO/dependabot/alerts

# https://docs.github.com/en/rest/repos/webhooks?apiVersion=2022-11-28

# https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#check-if-automated-security-fixes-are-enabled-for-a-repository

# https://api.github.com/repos/marketulinek/bookishop/vulnerability-alerts

# https://api.github.com/repos/marketulinek/bookishop/dependabot/alerts