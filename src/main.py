from config_manager import ConfigManager
from subscription_manager import SubscriptionManager
from update_retriever import UpdateRetriever
from data_processor import DataProcessor
from notifier import Notifier
from report_generator import ReportGenerator

def main():
    config_manager = ConfigManager()
    subscription_manager = SubscriptionManager()
    update_retriever = UpdateRetriever(config_manager.get_github_token())
    data_processor = DataProcessor()
    notifier = Notifier(config_manager.get_notification_settings())
    report_generator = ReportGenerator()

    repositories = subscription_manager.get_repositories()
    for repo in repositories:
        updates = update_retriever.get_latest_updates(repo)
        if updates:
            summary = data_processor.summarize_updates(updates)
            notifier.send_notification(summary)
            report_generator.generate_report(summary)

if __name__ == '__main__':
    main()
