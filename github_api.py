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

    class ApiRateLimitExceeded(Exception):
        pass

    def get_user_repos(self, username):
        """
        Retrieve repositories for a given GitHub username.

        :param username: GitHub username
        :return: List of repositories or None if an error occurs
        """
        url = self.URL_USER_REPOS.format(username)
        return self._request(url)

    def get_repo_pulls(self, username, reponame):
        """
        Retrieve pull requests for a given GitHub repository.

        :param username: GitHub username
        :param reponame: Repository name
        :return: List of pull requests or None if an error occurs
        """
        url = self.URL_REPO_PULLS.format(username, reponame)
        return self._request(url)

    def _request(self, url):
        """
        Make a request to the GitHub API.

        :param url: URL to request
        :return: Response JSON or None if an error occurs
        """
        if not self._rate_limit_ok():
            raise self.ApiRateLimitExceeded("GitHub API rate limit exceeded")

        response = self._make_api_request(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"GitHub API request failed with status code {response.status_code}")
            return None

    def _make_api_request(self, url):
        """
        Make a GET request to the specified URL.

        :param url: URL to request
        :return: Response object
        """
        return requests.get(url, headers=self.HEADERS)

    def _rate_limit_ok(self):
        """
        Check if the GitHub API rate limit is sufficient.

        :return: True if rate limit is sufficient, False otherwise
        """
        try:
            r = self._make_api_request(self.URL_RATE_LIMIT)
            rate_limit = int(r.json()['resources']['core']['remaining'])
            return rate_limit > 0
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while checking GitHub API rate limit: {e}")
            return False
