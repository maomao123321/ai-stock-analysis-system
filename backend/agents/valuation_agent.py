# backend/agents/valuation_agent.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp_client import get_mcp_tools, call_mcp_tool

def create_valuation_agent():
    """
    创建一个基于 ReAct 框架的估值分析代理。
    """
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    # 简化工具定义，假定 MCP Server 提供了这些工具
    def get_stock_valuation_tool(symbol: str):
        return call_mcp_tool('get_stock_valuation', symbol=symbol)

    tools = [get_stock_valuation_tool]
    
    system_prompt = """你是一位专业的股票估值分析师，擅长使用提供的工具对公司及其股价进行估值。
    你的任务是基于用户的输入，评估一家公司是否值得买入，并给出你的理由。
    请使用提供的工具获取所需数据，并以清晰、结构化的方式组织你的分析。
    """
    
    valuation_agent = create_react_agent(model, tools=tools, messages_modifier=[
        SystemMessage(content=system_prompt)
    ])
    
    return valuation_agent

if __name__ == '__main__':
    agent = create_valuation_agent()
    print("Valuation Agent created successfully.")

    