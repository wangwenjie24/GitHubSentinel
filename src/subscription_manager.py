import json

class SubscriptionManager:
    def __init__(self, subscriptions_file='config/subscriptions.json'):
        with open(subscriptions_file, 'r') as file:
            self.subscriptions = json.load(file)

    def get_repositories(self):
        return self.subscriptions.get('repositories', [])
