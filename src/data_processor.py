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

    def summarize_version(self, version_data):
        if not version_data:
            return "No release information available."

        summary = {
            'tag_name': version_data['tag_name'],
            'name': version_data['name'],
            'published_at': version_data['published_at'],
            'body': version_data['body']
        }
        return summary