import schedule
import time
import sys
import signal
from config_manager import ConfigManager
from subscription_manager import SubscriptionManager
from github_client import GithubClient
from report_generator import ReportGenerator
from notifier import Notifier
from llm import LLM
from logger import LOG


def graceful_shutdown(signum, frame):
    """
    优雅关闭程序的函数，处理信号时调用
    """
    LOG.info("[优雅退出]守护进程接收到终止信号")
    sys.exit(0)  # 安全退出程序


def github_job(subscription_manager, update_retriever, report_generator, notifier, days):
    """
    定时任务。
    """
    LOG.info("[开始执行定时任务]")
    subscriptions = subscription_manager.get_repositories()
    LOG.info(f"订阅列表：{subscriptions}")
    for repo in subscriptions:
        markdown_file_path = update_retriever.export_progress_by_date_range(repo, days)
        report_generator.generate_report_by_date_range(markdown_file_path, days)
    LOG.info(f"[定时任务执行完毕]")


def main():
    # 设置信号处理器
    signal.signal(signal.SIGTERM, graceful_shutdown)

    llm = LLM()
    config_manager = ConfigManager()
    subscription_manager = SubscriptionManager()
    update_retriever = GithubClient(config_manager.get_github_token())
    notifier = Notifier()
    report_generator = ReportGenerator(llm)

    # 从配置文件读取调度设置
    scheduler_settings = config_manager.get_scheduler_settings()
    frequency_days = scheduler_settings.get('frequency_days', '1')
    execution_time = scheduler_settings.get('execution_time', "08:00")

    github_job(subscription_manager, update_retriever, report_generator, notifier, frequency_days)

    schedule.every(frequency_days).days.at(
        execution_time
    ).do(github_job, subscription_manager, update_retriever, report_generator, notifier, frequency_days)

    """
    启动调度器，执行所有调度任务。
    """
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        LOG.error(f"主进程发生异常：{str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
