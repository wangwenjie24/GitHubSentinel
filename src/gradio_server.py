import gradio as gr

from config_manager import ConfigManager
from subscription_manager import SubscriptionManager
from report_generator import ReportGenerator
from notifier import Notifier
from llm import LLM
from update_retriever import UpdateRetriever

llm = LLM()
config_manager = ConfigManager()
subscription_manager = SubscriptionManager()
notifier = Notifier()
updateRetriever = UpdateRetriever()
report_generator = ReportGenerator(llm)

def generate_report_by_date_range(repo, days):
    markdown_file_path = report_generator.export_content_by_date_range(repo, days, updateRetriever)
    report, report_file_path = report_generator.generate_report_by_date_range(markdown_file_path, days)
    return report, report_file_path

# 创建Gradio界面
demo = gr.Interface(
    fn=generate_report_by_date_range,
    title="GitHubSentinel",
    inputs=[
        gr.Dropdown(
            subscription_manager.get_repositories(), label="订阅列表", info="已订阅GitHub项目"
        ),
        gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生成项目过去一段时间的进展，单位“天”")
    ],
    outputs=[gr.Markdown(), gr.File(label="下载报告")]
)

demo.launch()