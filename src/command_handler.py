class CommandHandler:
    def __init__(self, subscription_manager, update_retriever, report_generator):
        self.subscription_manager = subscription_manager
        self.update_retriever = update_retriever
        self.report_generator = report_generator

    def execute_command(self, command):
        if command.startswith('add'):
            repo = command.split(' ')[1]
            self.subscription_manager.add_repository(repo)
            print(f"Added subscription: {repo}")
        elif command.startswith('remove'):
            repo = command.split(' ')[1]
            self.subscription_manager.remove_repository(repo)
            print(f"Removed subscription: {repo}")
        elif command.startswith('export'):
            repo = command.split(' ')[1]
            self.update_retriever.export_daily_report(repo)
            print(f"Exported daily report for {repo}.")
        elif command == 'list':
            repos = self.subscription_manager.get_repositories()
            print("Subscribed repositories:")
            for repo in repos:
                print(repo)
        elif command == 'fetch':
            repos = self.subscription_manager.get_repositories()
            updates = []
            for repo in repos:
                updates.append(self.update_retriever.fetch_updates(repo))
            for update in updates:
                print(update)
        elif command == 'help':
            self.print_help()
        else:
            print("Invalid command. Type 'help' for available commands.")

    def print_help(self):
        """
        打印帮助信息，列出可用命令。
        """
        print("""
        GitHub Sentinel 使用指南:

        可用命令:
          add <repository>      - 增加一个GitHub仓库到订阅列表中
          remove <repository>   - 从订阅列表中删除一个GitHub仓库
          list                  - 列出所有当前订阅的仓库
          fetch                 - 立即获取所有订阅仓库的最新更新
          export                - 导出一个GitHub仓库的进展报告（issues 和 pull requests）
          help                  - 显示此帮助信息
          exit                  - 退出程序
        """)