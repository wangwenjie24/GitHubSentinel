import schedule
import time
from datetime import datetime

class Scheduler:
    def __init__(self, update_retriever, notifier, report_generator, subscription_manager):
        self.update_retriever = update_retriever
        self.notifier = notifier
        self.report_generator = report_generator
        self.subscription_manager = subscription_manager
        self.jobs = []

    def schedule_task(self, task, interval_type, interval_value):
        """
        添加调度任务。
        interval_type: 可以是 'daily', 'weekly', 'every'。
        interval_value: 表示间隔时间，比如天数或周数。
        """
        if interval_type == 'daily':
            job = schedule.every(interval_value).days.do(task)
        elif interval_type == 'weekly':
            job = schedule.every(interval_value).weeks.do(task)
        elif interval_type == 'every':
            job = schedule.every(interval_value).minutes.do(task)
        else:
            print(f"Unsupported interval type: {interval_type}")
            return

        self.jobs.append(job)
        print(f"Scheduled task: {task.__name__} ({interval_type} - {interval_value})")

    def fetch_and_generate_report(self):
        subscriptions = self.subscription_manager.get_repositories()
        for repo in subscriptions:
            updates = self.update_retriever.fetch_updates(repo)
            markdown_file_path = self.report_generator.generate_daily_report(repo, updates)
            self.report_generator.generate_formal_report(markdown_file_path)

    def run(self):
        """
        启动调度器，执行所有调度任务。
        """
        while True:
            schedule.run_pending()
            time.sleep(1)
