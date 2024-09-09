import threading
from config_manager import ConfigManager
from subscription_manager import SubscriptionManager
from update_retriever import UpdateRetriever
from report_generator import ReportGenerator
from scheduler import Scheduler
from notifier import Notifier
from llm import LLM

llm = LLM()
config_manager = ConfigManager()
subscription_manager = SubscriptionManager()
update_retriever = UpdateRetriever(config_manager.get_github_token())
notifier = Notifier()
report_generator = ReportGenerator(llm)

def run_scheduler(scheduler, interval_type, interval_value):
    # 让调度器在后台运行
    scheduler.schedule_task(scheduler.fetch_and_generate_report, interval_type, interval_value)
    scheduler.run()

def fetch_and_generate_report(self):
    subscriptions = subscription_manager.get_repositories()
    for repo in subscriptions:
        updates = update_retriever.fetch_updates(repo)
        markdown_file_path = report_generator.export_daily_content(repo, updates)
        report_generator.generate_daily_report(markdown_file_path)

def main():
    # 从配置文件读取调度设置
    scheduler_settings = config_manager.get_scheduler_settings()
    interval_type = scheduler_settings.get('interval_type', 'daily')
    interval_value = scheduler_settings.get('interval_value', 1)

    # 创建调度器线程，让它在后台运行
    scheduler_thread = threading.Thread(target=run_scheduler, args=(Scheduler(), interval_type, interval_value))
    scheduler_thread.daemon = True  # 设置为守护线程，主线程退出后自动关闭
    scheduler_thread.start()

if __name__ == '__main__':
    main()
