from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class LLM:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")

    def summarize_issues_and_prs(self, markdown_content, dry_run=False):
        """
        使用 GPT-4 API 整理 issues 和 pull requests 列表并生成总结。
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "你是一个负责项目报告生成的助手。"),
                ("user", "以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"),
            ]
        )

        if dry_run:
            print(markdown_content)
            return "dry run"

        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"markdown_content": markdown_content})
        return result
