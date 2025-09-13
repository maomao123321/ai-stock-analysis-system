# backend/mcp_client.py
import requests
import json

MCP_SERVER_URL = "http://mcp_server:8001"

def get_mcp_tools():
    """
    从 MCP Server 获取可用工具列表。
    """
    try:
        response = requests.get(f"{MCP_SERVER_URL}/tools")
        response.raise_for_status()
        return response.json()["tools"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tools from MCP server: {e}")
        return []

def call_mcp_tool(tool_name: str, **kwargs):
    """
    调用 MCP Server 上的指定工具。
    """
    try:
        response = requests.post(f"{MCP_SERVER_URL}/call_tool", params={"tool_name": tool_name}, json=kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling tool on MCP server: {e}")
        return {"error": str(e)}