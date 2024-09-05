import threading
import time
from config_manager import ConfigManager
from subscription_manager import SubscriptionManager
from update_retriever import UpdateRetriever
from data_processor import DataProcessor
from report_generator import ReportGenerator
from scheduler import Scheduler
from command_handler import CommandHandler

def run_scheduler(scheduler, interval_type, interval_value):
    # 让调度器在后台运行
    scheduler.schedule_task(fetch_and_generate_report, interval_type, interval_value)
    scheduler.run()

def fetch_and_generate_report():
    # 立即获取并生成报告
    config_manager = ConfigManager()
    subscription_manager = SubscriptionManager()
    update_retriever = UpdateRetriever(config_manager.get_github_token())
    data_processor = DataProcessor()
    report_generator = ReportGenerator()

    repositories = subscription_manager.get_repositories()
    for repo in repositories:
        version_data = update_retriever.get_latest_version(repo)
        if version_data:
            summary = data_processor.summarize_version(version_data)
            report_generator.generate_report(summary)

if __name__ == '__main__':
    config_manager = ConfigManager()
    subscription_manager = SubscriptionManager()
    update_retriever = UpdateRetriever(config_manager.get_github_token())
    data_processor = DataProcessor()
    report_generator = ReportGenerator()

    command_handler = CommandHandler(subscription_manager, update_retriever, data_processor, report_generator)

    scheduler = Scheduler()

    # 从配置文件读取调度设置
    scheduler_settings = config_manager.get_scheduler_settings()
    interval_type = scheduler_settings.get('interval_type', 'daily')
    interval_value = scheduler_settings.get('interval_value', 1)

    # 创建调度器线程，让它在后台运行
    scheduler_thread = threading.Thread(target=run_scheduler, args=(scheduler, interval_type, interval_value))
    scheduler_thread.daemon = True  # 设置为守护线程，主线程退出后自动关闭
    scheduler_thread.start()

    # 打印帮助信息
    command_handler.print_help()

    # 主循环，接受用户输入
    while True:
        command = input("Enter command (add/remove/list/fetch/exit): ").strip()
        if command == 'exit':
            print("Exiting program.")
            break
        else:
            command_handler.execute_command(command)

        # 确保调度器线程在后台继续运行
        time.sleep(1)
