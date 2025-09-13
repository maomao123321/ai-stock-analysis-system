# mcp_server/main.py
from fastapi import FastAPI
from mcp_server.tools import get_company_overview, get_stock_price

app = FastAPI()

@app.get("/tools")
def get_available_tools():
    """
    返回所有可用的工具列表，供 Agent 调用。
    """
    return {
        "tools": [
            {
                "name": "get_company_overview",
                "description": "获取公司的基本面概览",
                "parameters": {"type": "object", "properties": {"symbol": {"type": "string"}}},
            },
            {
                "name": "get_stock_price",
                "description": "获取股票实时价格",
                "parameters": {"type": "object", "properties": {"symbol": {"type": "string"}}},
            },
        ]
    }

@app.post("/call_tool")
def call_tool(tool_name: str, params: dict):
    """
    根据 Agent 的请求，执行相应的工具函数。
    """
    if tool_name == "get_company_overview":
        return get_company_overview(**params)
    elif tool_name == "get_stock_price":
        return get_stock_price(**params)
    else:
        return {"error": "Tool not found."}