class Notifier:
    def __init__(self, settings):
        self.settings = settings

    def send_notification(self, summary):
        # 这里可以集成邮件、Slack或其他通知方式
        for item in summary:
            print(f"Commit: {item['message']}, Author: {item['author']}, Date: {item['date']}")
