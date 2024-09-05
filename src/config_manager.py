import json
import os

class ConfigManager:
    def __init__(self, config_file='../config/config.json'):
        with open(config_file, 'r') as file:
            self.config = json.load(file)

    def get_github_token(self):
        print(os.getenv('GITHUB_TOKEN', self.config.get('github_token')))
        # 优先从环境变量获取 GitHub Token
        return os.getenv('GITHUB_TOKEN', self.config.get('github_token'))

    def get_notification_settings(self):
        return self.config.get('notification_settings')

    def get_scheduler_settings(self):
        return self.config.get('scheduler_settings')