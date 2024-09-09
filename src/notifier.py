import json


class Notifier:
    def __init__(self, config_file='../config.json'):
        with open(config_file, 'r') as file:
            self.config = json.load(file)

    def send_notification(self, summary):
        for item in summary:
            print(f"Commit: {item['message']}, Author: {item['author']}, Date: {item['date']}")
