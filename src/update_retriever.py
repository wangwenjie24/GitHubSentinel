import requests

class UpdateRetriever:
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.github.com/repos/'

    def get_latest_updates(self, repo_name):
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(f'{self.api_url}{repo_name}/commits', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_latest_version(self, repo_name):
        headers = {'Authorization': f'token {self.token}'}
        # 获取最新的版本信息（包括 release 和 tags）
        response = requests.get(f'{self.api_url}{repo_name}/releases/latest', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch latest release for {repo_name}: {response.status_code}")
            return None
