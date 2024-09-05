class Notifier:
    def __init__(self, settings):
        self.settings = settings

    def send_notification(self, summary):
        # ������Լ����ʼ���Slack������֪ͨ��ʽ
        for item in summary:
            print(f"Commit: {item['message']}, Author: {item['author']}, Date: {item['date']}")
