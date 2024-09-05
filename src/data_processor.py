class DataProcessor:
    def summarize_updates(self, updates):
        summary = []
        for update in updates:
            commit = update['commit']
            summary.append({
                'message': commit['message'],
                'author': commit['author']['name'],
                'date': commit['author']['date']
            })
        return summary
