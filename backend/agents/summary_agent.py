# backend/agents/summary_agent.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

def create_summary_agent():
    """
    创建一个总结代理，用于将其他代理的分析结果整合成最终报告。
    """
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    def generate_report(analysis_results: dict):
        """
        根据分析结果，生成最终的 Markdown 报告。
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="你是一位专业的金融报告撰写人，请根据提供的分析结果，撰写一份完整、清晰的股票分析报告，并以Markdown格式输出。"),
            HumanMessage(content=f"请根据以下分析结果撰写报告：\n{analysis_results}")
        ])
        
        chain = prompt | model
        report = chain.invoke({"analysis_results": analysis_results})
        
        return report.content

    return generate_report

if __name__ == '__main__':
    agent = create_summary_agent()
    print("Summary Agent created successfully.")