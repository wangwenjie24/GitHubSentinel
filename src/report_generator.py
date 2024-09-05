class ReportGenerator:
    def generate_report(self, summary, report_file='report.txt'):
        with open(report_file, 'w') as file:
            for item in summary:
                file.write(f"Commit: {item['message']}, Author: {item['author']}, Date: {item['date']}
")
