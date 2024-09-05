class ReportGenerator:
    def generate_report(self, summary, report_file='report.txt'):
        with open(report_file, 'w') as file:
            file.write(f"Latest Version: {summary['name']} ({summary['tag_name']})\n")
            file.write(f"Published At: {summary['published_at']}\n\n")
            file.write("Release Notes:\n")
            file.write(f"{summary['body']}\n")
        print(f"Report generated: {report_file}")
