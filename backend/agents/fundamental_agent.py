# backend/agents/fundamental_agent.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# 假设 mcp_client.py 已经实现
from mcp_client import get_mcp_tools, call_mcp_tool

def create_fundamental_agent():
    """
    创建一个基于 ReAct 框架的基本面分析代理。
    """
    # 1. 加载语言模型
    # 这里我们使用 ChatOpenAI，你需要确保 OPENAI_API_KEY 环境变量已设置
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    # 2. 定义工具
    # 我们从 MCP Server 获取工具，并将其包装为 LangChain 可用的格式
    mcp_tools = get_mcp_tools()
    
    # 确保我们只获取基本面分析相关的工具
    fundamental_tools = []
    for tool in mcp_tools:
        if tool['name'] in ['get_company_overview', 'get_stock_financials']:
            # 将 MCP 工具包装成 LangChain 工具
            # 注意：这里需要一个更复杂的包装逻辑来将 MCP 调用与 LangChain 工具类连接起来
            # 我们先用一个简化的方式来演示
            pass

    # 简化的工具定义
    def get_company_overview_tool(symbol: str):
        return call_mcp_tool('get_company_overview', symbol=symbol)

    def get_stock_financials_tool(symbol: str):
        return call_mcp_tool('get_stock_financials', symbol=symbol)

    tools = [get_company_overview_tool, get_stock_financials_tool]
    
    # 3. 构建详细的分析 Prompt
    # 这个 Prompt 将指导代理如何思考和行动
    system_prompt = """你是一位专业的基本面分析师，擅长使用提供的工具分析公司的财务状况。
    你的任务是基于用户的输入，完成以下维度的详细分析：
    - 公司信息概览
    - 财务报表（收入、利润、资产负债）
    - 盈利能力（ROE, ROA, 毛利率）
    - 成长能力（收入增长率, 净利润增长率）
    - 营运能力（存货周转率, 应收账款周转率）
    - 偿债能力（资产负债率）
    - 现金流状况
    - 杜邦分析
    
    请使用提供的工具获取所需数据，并以清晰、结构化的方式组织你的分析。
    """
    
    # 4. 创建 ReAct Agent
    # LangGraph 将自动处理“思考-行动”的循环
    fundamental_agent = create_react_agent(model, tools=tools, messages_modifier=[
        SystemMessage(content=system_prompt)
    ])
    
    return fundamental_agent

if __name__ == '__main__':
    # 这是一个简单的测试，确保代理可以被创建
    agent = create_fundamental_agent()
    print("Fundamental Agent created successfully.")