import json

class ConfigManager:
    def __init__(self, config_file='config/config.json'):
        with open(config_file, 'r') as file:
            self.config = json.load(file)

    def get_github_token(self):
        return self.config.get('github_token')

    def get_notification_settings(self):
        return self.config.get('notification_settings')
