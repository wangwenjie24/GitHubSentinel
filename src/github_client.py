import os
import requests
from datetime import datetime, date, timedelta
from logger import LOG


class GithubClient:
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

    def export_progress_by_date_range(self, repo, days):
        """
        导出时间范围内进展报告（issues 和 pull requests）到 Markdown 文件。
        """
        # 校验文件是否存在
        repo_dir = f'../report/{repo.replace('/', '_')}'
        os.makedirs(repo_dir, exist_ok=True)

        # 获取指定日期范围内的更新
        today = datetime.today()
        since = today - timedelta(days=days)
        updates = self.fetch_updates(repo, since=since.isoformat(), until=today.isoformat())

        # 构建文件路径
        date_str = f"{since.strftime("%Y-%m-%d")}_to_{today.strftime("%Y-%m-%d")}"
        markdown_file_path = repo_dir + '/' + date_str + '.md'

        # 写入文件
        with open(markdown_file_path, 'w', encoding="utf-8") as f:
            f.write(f"# Progress for {repo} ({since.strftime("%Y-%m-%d")} to {today.strftime("%Y-%m-%d")})\n\n")
            f.write(f"\n## Issues Closed in the Last {days} Days\n")
            if updates["issues"]:
                for issue in updates["issues"]:
                    f.write(f"- {issue['title']} (#{issue['number']})\n")

        LOG.info(f"[{repo}]项目最新进展文件生成： {markdown_file_path}")  # 记录日志
        return markdown_file_path

