import os
import requests

class UpdateRetriever:
    def __init__(self, token=None):
        self.base_url = "https://api.github.com"
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def fetch_updates(self, repo, since, until):
        """
        获取更新内容列表。
        """
        updates = {
            "issues": self.fetch_issues(repo),
            "pull_requests": self.fetch_pull_requests(repo),
        }
        return updates

    def fetch_issues(self, repo, since=None, until=None):
        """
        获取指定仓库的 issues 列表。
        """
        url = f"{self.base_url}/repos/{repo}/issues"
        params = {
            "since": since,
            "until": until,
            "state": "closed"
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch issues for {repo}: {response.status_code}")
            return []

    def fetch_pull_requests(self, repo, since=None, until=None):
        """
        获取指定仓库的 pull requests 列表。
        """
        url = f"{self.base_url}/repos/{repo}/pulls"
        params = {
            "since": since,
            "until": until,
            "state": "closed"
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch pull requests for {repo}: {response.status_code}")
            return []