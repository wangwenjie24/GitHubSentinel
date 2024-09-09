from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class LLM:
    def __init__(self):
        # 创建OpenAI实例
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        # 从文件中读取系统提示词
        with open("../prompts/report_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def summarize_issues_and_prs(self, markdown_content, dry_run=False):
        """
        使用 GPT-4 API 整理 issues 和 pull requests 列表并生成总结。
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("user", "{markdown_content}"),
            ]
        )

        if dry_run:
            print(markdown_content)
            return "dry run"

        # 调用模型生成内容
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"markdown_content": markdown_content})
