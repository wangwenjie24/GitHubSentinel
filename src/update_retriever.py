import os
import requests
from datetime import datetime
class UpdateRetriever:
    def __init__(self, token=None):
        self.base_url = "https://api.github.com"
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def fetch_updates(self, repo):
        updates= {
            "commits": self.fetch_commits(repo),
            "issues": self.fetch_issues(repo),
            "pull_requests": self.fetch_pull_requests(repo),
        }
        return updates

    def fetch_commits(self, repo):
        """
        获取指定仓库的 issues 列表。
        """
        url = f"{self.base_url}/repos/{repo}/commits"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch issues for {repo}: {response.status_code}")
            return []

    def fetch_issues(self, repo):
        """
        获取指定仓库的 issues 列表。
        """
        url = f"{self.base_url}/repos/{repo}/issues"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch issues for {repo}: {response.status_code}")
            return []

    def fetch_pull_requests(self, repo):
        """
        获取指定仓库的 pull requests 列表。
        """
        url = f"{self.base_url}/repos/{repo}/pulls"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch pull requests for {repo}: {response.status_code}")
            return []

    def export_daily_report(self, repo):
        """
        导出每日进展报告（issues 和 pull requests）到 Markdown 文件。
        """
        issues = self.fetch_issues(repo)
        pull_requests = self.fetch_pull_requests(repo)

        # 创建 Markdown 文件
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_name = f"{repo.replace('/', '_')}_{date_str}.md"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"# {repo} Daily Report - {date_str}\n\n")
            f.write("## Issues\n")
            if issues:
                for issue in issues:
                    f.write(f"- {issue['title']} (#{issue['number']})\n")
            else:
                f.write("No open issues.\n")
            f.write("\n## Pull Requests\n")
            if pull_requests:
                for pr in pull_requests:
                    f.write(f"- {pr['title']} (#{pr['number']})\n")
            else:
                f.write("No open pull requests.\n")

        print(f"Daily report exported: {file_name}")