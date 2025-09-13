# mcp_server/tools.py
import os
import requests
from typing import Dict, List, Any

# 从环境变量中获取 Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")

def get_company_overview(symbol: str) -> Dict[str, Any]:
    """
    获取公司基本面信息，包括财务状况、高管信息等。
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"error": "ALPHA_VANTAGE_API_KEY is not set."}

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    return response.json()

def get_stock_price(symbol: str) -> Dict[str, Any]:
    """
    获取股票实时价格。
    """
    if not ALPHA_VANTAGE_API_KEY:
        return {"error": "ALPHA_VANTAGE_API_KEY is not set."}

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    return response.json()

# 你可以继续添加其他工具函数，比如获取历史K线、财报数据等
# 例如：
# def get_stock_financials(symbol: str):
#     url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
#     ...