import os
from datetime import date
from llm import LLM
class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_daily_report(self, repo, updates):
        file_path = f'daily_progress/{repo.replace("/", "_")}_{date.today()}.md'
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

    def generate_formal_report(self, markdown_file):
        """
        调用 GPT-4 API 将 issues 和 pull requests 整理成正式报告。
        """
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        summary = self.llm.summarize_issues_and_prs(content, False)
        file_name = markdown_file.replace(".md", "_report.md")

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(summary)

        print(f"Formal report generated: {file_name}")