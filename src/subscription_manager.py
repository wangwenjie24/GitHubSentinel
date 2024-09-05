import json

class SubscriptionManager:

    def __init__(self, subscription_file='../config/subscriptions.json'):
        self.subscription_file = subscription_file
        self.subscriptions = self._load_subscriptions()

    def _load_subscriptions(self):
        """
        从 JSON 文件中加载订阅信息。
        """
        try:
            with open(self.subscription_file, 'r') as file:
                return json.load(file).get('repositories', [])
        except FileNotFoundError:
            return []

    def _save_subscriptions(self):
        """
        将当前订阅列表保存到 JSON 文件中。
        """
        with open(self.subscription_file, 'w') as file:
            json.dump({"repositories": self.subscriptions}, file, indent=4)

    def get_repositories(self):
        """
        获取当前订阅的仓库列表。
        """
        return self.subscriptions

    def add_repository(self, repo):
        """
        增加订阅的仓库并更新文件。
        """
        if repo not in self.subscriptions:
            self.subscriptions.append(repo)
            self._save_subscriptions()
            print(f"Successfully added {repo} to subscriptions.")
        else:
            print(f"{repo} is already in the subscription list.")

    def remove_repository(self, repo):
        """
        删除订阅的仓库并更新文件。
        """
        if repo in self.subscriptions:
            self.subscriptions.remove(repo)
            self._save_subscriptions()
            print(f"Successfully removed {repo} from subscriptions.")
        else:
            print(f"{repo} is not in the subscription list.")