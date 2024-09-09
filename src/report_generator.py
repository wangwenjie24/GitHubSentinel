from logger import LOG


class ReportGenerator:
    def __init__(self, llm):
        self.llm = llm

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

        LOG.info(f"GitHub 项目报告已保存到 {report_file_path}")

        return report, report_file_path