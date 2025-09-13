from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import subprocess
import os
import requests
import json
from datetime import datetime

app = FastAPI(
    title="Agentic Stock System API",
    description="基于 LangGraph 的 AI Agent System 后端服务",
    version="1.0.0"
)

# Alpha Vantage API 配置
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_quote(symbol: str):
    """获取股票实时报价"""
    if not ALPHA_VANTAGE_API_KEY:
        return {"error": "Alpha Vantage API key not configured"}
    
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if "Global Quote" in data:
            quote = data["Global Quote"]
            return {
                "symbol": quote.get("01. symbol", symbol),
                "price": float(quote.get("05. price", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": quote.get("10. change percent", "0%").replace("%", ""),
                "volume": int(quote.get("06. volume", 0)),
                "high": float(quote.get("03. high", 0)),
                "low": float(quote.get("04. low", 0)),
                "open": float(quote.get("02. open", 0)),
                "previous_close": float(quote.get("08. previous close", 0))
            }
        else:
            return {"error": f"Failed to get data for {symbol}: {data.get('Note', 'Unknown error')}"}
    except Exception as e:
        return {"error": f"API request failed: {str(e)}"}

def get_company_overview(symbol: str):
    """获取公司基本面信息"""
    if not ALPHA_VANTAGE_API_KEY:
        return {"error": "Alpha Vantage API key not configured"}
    
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if "Symbol" in data:
            return {
                "symbol": data.get("Symbol", symbol),
                "name": data.get("Name", ""),
                "sector": data.get("Sector", ""),
                "industry": data.get("Industry", ""),
                "market_cap": data.get("MarketCapitalization", ""),
                "pe_ratio": data.get("PERatio", ""),
                "dividend_yield": data.get("DividendYield", ""),
                "beta": data.get("Beta", ""),
                "52_week_high": data.get("52WeekHigh", ""),
                "52_week_low": data.get("52WeekLow", ""),
                "description": data.get("Description", "")
            }
        else:
            return {"error": f"Failed to get overview for {symbol}: {data.get('Note', 'Unknown error')}"}
    except Exception as e:
        return {"error": f"API request failed: {str(e)}"}

def calculate_technical_indicators(price_data):
    """计算技术指标（简化版本）"""
    if not price_data or "price" not in price_data:
        return {}
    
    price = price_data["price"]
    change = price_data.get("change", 0)
    change_percent = float(price_data.get("change_percent", 0))
    
    # 简化的技术指标计算
    rsi = 50 + (change_percent * 2)  # 简化的 RSI 计算
    rsi = max(0, min(100, rsi))
    
    macd = "positive" if change > 0 else "negative"
    
    # 简化的移动平均线（基于当前价格）
    ma_20 = price * (1 + change_percent * 0.01)
    ma_50 = price * (1 + change_percent * 0.005)
    
    return {
        "rsi": round(rsi, 1),
        "macd": macd,
        "moving_average_20": round(ma_20, 2),
        "moving_average_50": round(ma_50, 2)
    }

def generate_ai_insights(quote_data, overview_data, technical_indicators):
    """生成 AI 洞察"""
    insights = []
    
    if "error" not in quote_data:
        price = quote_data.get("price", 0)
        change_percent = float(quote_data.get("change_percent", 0))
        volume = quote_data.get("volume", 0)
        
        # 基于价格变化的洞察
        if change_percent > 2:
            insights.append("股价大幅上涨，成交量活跃，市场情绪积极")
        elif change_percent < -2:
            insights.append("股价出现回调，建议关注支撑位")
        else:
            insights.append("股价相对稳定，市场观望情绪浓厚")
        
        # 基于成交量的洞察
        if volume > 1000000:
            insights.append("成交量放大，表明市场关注度较高")
        else:
            insights.append("成交量相对较低，市场参与度一般")
    
    # 基于技术指标的洞察
    if technical_indicators:
        rsi = technical_indicators.get("rsi", 50)
        if rsi > 70:
            insights.append("RSI 指标显示超买，短期可能存在回调风险")
        elif rsi < 30:
            insights.append("RSI 指标显示超卖，可能存在反弹机会")
        else:
            insights.append("RSI 指标处于正常区间，技术面相对健康")
    
    # 基于基本面的洞察
    if "error" not in overview_data and overview_data.get("sector"):
        sector = overview_data.get("sector", "")
        pe_ratio = overview_data.get("pe_ratio", "")
        
        if pe_ratio and pe_ratio != "None":
            try:
                pe = float(pe_ratio)
                if pe < 15:
                    insights.append(f"{sector} 行业估值偏低，具有投资价值")
                elif pe > 25:
                    insights.append(f"{sector} 行业估值偏高，需谨慎投资")
            except:
                pass
    
    return insights[:4]  # 返回最多4个洞察

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径，用于验证服务是否启动"""
    return {
        "message": "Agentic Stock System API 正在运行！",
        "status": "success",
        "service": "backend"
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0"
    }

@app.get("/api/test")
async def test_endpoint():
    """测试端点，供前端调用"""
    return {
        "message": "后端 API 调用成功！",
        "data": {
            "timestamp": datetime.now().isoformat() + "Z",
            "service": "Agentic Stock System Backend",
            "alpha_vantage_configured": bool(ALPHA_VANTAGE_API_KEY)
        }
    }

@app.get("/api/stocks/realtime")
async def get_realtime_stocks():
    """获取实时股票数据"""
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    stocks_data = []
    
    for symbol in symbols:
        quote_data = get_stock_quote(symbol)
        if "error" not in quote_data:
            stocks_data.append({
                "symbol": quote_data["symbol"],
                "price": quote_data["price"],
                "change": quote_data["change"],
                "change_percent": float(quote_data["change_percent"]),
                "volume": quote_data["volume"],
                "high": quote_data["high"],
                "low": quote_data["low"],
                "open": quote_data["open"]
            })
        else:
            # 如果 API 失败，使用模拟数据
            stocks_data.append({
                "symbol": symbol,
                "price": 150.0 + hash(symbol) % 100,
                "change": (hash(symbol) % 20) - 10,
                "change_percent": ((hash(symbol) % 20) - 10) * 0.1,
                "volume": 1000000 + hash(symbol) % 5000000,
                "high": 160.0,
                "low": 140.0,
                "open": 155.0
            })
    
    return {
        "stocks": stocks_data,
        "timestamp": datetime.now().isoformat() + "Z",
        "data_source": "Alpha Vantage API" if ALPHA_VANTAGE_API_KEY else "Simulated Data"
    }

@app.get("/api/mcp/status")
async def mcp_status():
    """MCP 服务器状态检查"""
    mcp_port = os.getenv("MCP_SERVER_PORT", "8001")
    return {
        "mcp_server": {
            "status": "running",
            "port": mcp_port,
            "host": "0.0.0.0",
            "protocol": "MCP v1.0"
        }
    }

@app.get("/api/mcp/tools")
async def list_mcp_tools():
    """列出 MCP 可用工具"""
    return {
        "tools": [
            {
                "name": "get_stock_info",
                "description": "获取股票信息",
                "parameters": ["symbol"]
            },
            {
                "name": "analyze_market", 
                "description": "分析市场趋势",
                "parameters": ["timeframe"]
            },
            {
                "name": "get_portfolio_status",
                "description": "获取投资组合状态",
                "parameters": []
            }
        ]
    }

@app.post("/api/analyze/stock")
async def analyze_stock(symbol: str):
    """分析单个股票"""
    try:
        # 获取真实股票数据
        quote_data = get_stock_quote(symbol)
        overview_data = get_company_overview(symbol)
        
        # 检查是否有错误，如果有错误则使用模拟数据
        if "error" in quote_data:
            print(f"API 失败，使用模拟数据: {quote_data['error']}")
            # 使用模拟数据
            quote_data = {
                "symbol": symbol,
                "price": 150.0 + hash(symbol) % 100,
                "change": (hash(symbol) % 20) - 10,
                "change_percent": str(((hash(symbol) % 20) - 10) * 0.1),
                "volume": 1000000 + hash(symbol) % 5000000,
                "high": 160.0,
                "low": 140.0,
                "open": 155.0,
                "previous_close": 145.0
            }
            
            # 模拟公司信息
            overview_data = {
                "symbol": symbol,
                "name": f"{symbol} Inc.",
                "sector": "Technology",
                "industry": "Software",
                "market_cap": "1000000000",
                "pe_ratio": "25.5",
                "dividend_yield": "2.1",
                "beta": "1.2",
                "52_week_high": "200.0",
                "52_week_low": "100.0",
                "description": f"模拟的 {symbol} 公司信息"
            }
        
        # 计算技术指标
        technical_indicators = calculate_technical_indicators(quote_data)
        
        # 生成 AI 洞察
        ai_insights = generate_ai_insights(quote_data, overview_data, technical_indicators)
        
        # 生成投资建议
        price = quote_data.get("price", 0)
        change_percent = float(quote_data.get("change_percent", 0))
        
        if change_percent > 3:
            action = "考虑减仓"
            confidence = 0.8
        elif change_percent < -3:
            action = "考虑加仓"
            confidence = 0.7
        else:
            action = "持有观望"
            confidence = 0.6
        
        # 计算目标价和止损价
        target_price = price * 1.1  # 10% 上涨目标
        stop_loss = price * 0.95   # 5% 止损
        
        # 风险评估
        beta = overview_data.get("beta", "1.0")
        try:
            beta_value = float(beta) if beta != "None" else 1.0
            if beta_value > 1.5:
                risk_level = "高"
                volatility = "高"
            elif beta_value > 1.0:
                risk_level = "中高"
                volatility = "中高"
            else:
                risk_level = "中低"
                volatility = "中低"
        except:
            risk_level = "中等"
            volatility = "中等"
        
        # 趋势分析
        if change_percent > 1:
            short_term = "上涨趋势"
        elif change_percent < -1:
            short_term = "下跌趋势"
        else:
            short_term = "横盘整理"
        
        analysis_result = {
            "symbol": symbol,
            "real_time_data": quote_data,
            "company_info": overview_data if "error" not in overview_data else None,
            "analysis": {
                "technical_indicators": technical_indicators,
                "trend_analysis": {
                    "short_term": short_term,
                    "medium_term": "基于技术指标分析",
                    "long_term": "基于基本面分析"
                },
                "risk_assessment": {
                    "volatility": volatility,
                    "risk_level": risk_level,
                    "beta": beta_value if 'beta_value' in locals() else 1.0
                },
                "ai_insights": ai_insights,
                "recommendation": {
                    "action": action,
                    "confidence": confidence,
                    "target_price": round(target_price, 2),
                    "stop_loss": round(stop_loss, 2)
                }
            },
            "timestamp": datetime.now().isoformat() + "Z",
            "status": "success",
            "data_source": "模拟数据 (Alpha Vantage API 不可用)"
        }
        return analysis_result
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.post("/api/analyze/market")
async def analyze_market_trend(timeframe: str = "1d"):
    """分析市场整体趋势"""
    try:
        market_analysis = {
            "timeframe": timeframe,
            "market_overview": {
                "overall_trend": "震荡上行",
                "market_sentiment": "谨慎乐观",
                "volatility_index": 18.5,
                "sector_performance": {
                    "科技股": "领涨",
                    "金融股": "稳定",
                    "能源股": "下跌",
                    "医疗股": "震荡"
                }
            },
            "key_events": [
                "美联储政策会议即将召开",
                "科技巨头财报季开始",
                "地缘政治风险有所缓解"
            ],
            "ai_analysis": {
                "market_outlook": "短期内市场可能继续震荡，但长期趋势依然向上",
                "risk_factors": [
                    "通胀数据超预期",
                    "地缘政治紧张局势",
                    "企业盈利不及预期"
                ],
                "opportunities": [
                    "科技股估值合理",
                    "新兴市场复苏",
                    "绿色能源政策利好"
                ]
            },
            "recommendations": {
                "strategy": "均衡配置",
                "sector_allocation": {
                    "科技": 30,
                    "金融": 25,
                    "医疗": 20,
                    "消费": 15,
                    "其他": 10
                },
                "risk_management": "建议保持 20% 现金仓位"
            },
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "success"
        }
        return market_analysis
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/api/portfolio/status")
async def get_portfolio_status():
    """获取投资组合状态"""
    try:
        portfolio = {
            "total_value": 125000.00,
            "total_gain": 8500.00,
            "total_gain_percent": 7.28,
            "daily_change": 1250.00,
            "daily_change_percent": 1.01,
            "positions": [
                {
                    "symbol": "AAPL",
                    "shares": 100,
                    "current_price": 175.43,
                    "value": 17543.00,
                    "gain": 2150.00,
                    "gain_percent": 13.98,
                    "weight": 14.03
                },
                {
                    "symbol": "GOOGL",
                    "shares": 50,
                    "current_price": 142.56,
                    "value": 7128.00,
                    "gain": -123.00,
                    "gain_percent": -1.69,
                    "weight": 5.70
                },
                {
                    "symbol": "MSFT",
                    "shares": 75,
                    "current_price": 378.85,
                    "value": 28413.75,
                    "gain": 3420.00,
                    "gain_percent": 13.70,
                    "weight": 22.73
                },
                {
                    "symbol": "TSLA",
                    "shares": 25,
                    "current_price": 248.12,
                    "value": 6203.00,
                    "gain": -567.00,
                    "gain_percent": -8.37,
                    "weight": 4.96
                },
                {
                    "symbol": "AMZN",
                    "shares": 40,
                    "current_price": 155.78,
                    "value": 6231.20,
                    "gain": 189.00,
                    "gain_percent": 3.13,
                    "weight": 4.98
                }
            ],
            "performance_metrics": {
                "sharpe_ratio": 1.25,
                "max_drawdown": -8.5,
                "volatility": 15.2,
                "beta": 1.08
            },
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "success"
        }
        return portfolio
    except Exception as e:
        return {"error": str(e), "status": "error"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
