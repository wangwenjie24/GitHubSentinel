import threading
import time
from config_manager import ConfigManager
from subscription_manager import SubscriptionManager
from update_retriever import UpdateRetriever
from report_generator import ReportGenerator
from scheduler import Scheduler
from command_handler import CommandHandler
from notifier import Notifier
from llm import LLM

def main():
    llm = LLM()
    config_manager = ConfigManager()
    subscription_manager = SubscriptionManager()
    update_retriever = UpdateRetriever(config_manager.get_github_token())
    notifier = Notifier()
    report_generator = ReportGenerator(llm)

    command_handler = CommandHandler(subscription_manager, update_retriever, report_generator)

    # 打印帮助信息
    command_handler.print_help()

    # 主循环，接受用户输入
    while True:
        command = input("Enter command (add/remove/list/fetch/export/exit): ").strip()
        if command == 'exit':
            print("Exiting program.")
            break
        else:
            command_handler.execute_command(command)

if __name__ == '__main__':
    main()
