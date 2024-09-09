import os
from datetime import date
from datetime import datetime, timedelta

class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

    def format_date(self, date):
        # 格式化日期为 YYYY-MM-DD
        formatted_date = date.strftime("%Y-%m-%d")
        return formatted_date

    def export_content_by_date_range(self, repo, days, updateRetriever):
        """
        导出时间范围内进展报告（issues 和 pull requests）到 Markdown 文件。
        """
        today = datetime.today()
        since = today - timedelta(days=days)

        # 校验文件是否存在
        repo_dir = f'../report/{repo.replace('/', '_')}'
        os.makedirs(repo_dir, exist_ok=True)

        # 获取更新内容
        updates = updateRetriever.fetch_updates(repo, since=since.isoformat(), until=today.isoformat())

        # 创建 Markdown 文件
        date_str = f"{self.format_date(since)}_to_{self.format_date(today)}"
        file_path = repo_dir + '/' + date_str + '.md'


        ## 写入文件
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(f"# Progress for {repo} ({self.format_date(since)} to {self.format_date(today)})\n\n")
            f.write(f"\n## Issues Closed in the Last {days} Days\n")
            f.write("## Issues\n")
            if updates["issues"]:
                for issue in updates["issues"]:
                    f.write(f"- {issue['title']} (#{issue['number']})\n")

        print(f"Daily report exported: {file_path}")
        return file_path

    def generate_report_by_date_range(self, markdown_file_path, days):
        """
        调用 GPT-4 API 将 issues 和 pull requests 整理成正式报告。
        """
        # 读取content文件
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 调用模型生成总结
        report = self.llm.summarize_issues_and_prs(content, False)

        # 输出文档
        report_file_path = markdown_file_path.replace(".md", "_report.md")
        with open(report_file_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"Formal report generated: {report_file_path}")

        return report, report_file_path

    def export_daily_content(self, repo, updates):
        file_path = f'../daily_progress/{repo.replace("/", "_")}_{date.today()}.md'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# Daily Progress for {repo} ({date.today()})\n\n")
            # file.write("## Commits\n")
            # for commit in updates['commits']:
            #     file.write(f"- {commit}\n")
            file.write("\n## Issues\n")
            for issue in updates['issues']:
                file.write(f"- {issue['title']}\n")
            file.write("\n## Pull Requests\n")
            for pr in updates['pull_requests']:
                file.write(f"- {pr['title']}\n")
        return file_path

    def generate_daily_report(self, markdown_file_path):
        """
        调用 GPT-4 API 将 issues 和 pull requests 整理成正式报告。
        """
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        summary = self.llm.summarize_issues_and_prs(content, False)
        file_name = markdown_file_path.replace(".md", "_report.md")

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(summary)

        print(f"Formal report generated: {file_name}")