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
