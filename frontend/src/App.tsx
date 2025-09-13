import axios from 'axios'
import {
    Activity,
    AlertCircle,
    BarChart3,
    CheckCircle,
    Database,
    DollarSign,
    RefreshCw,
    Server,
    Settings,
    TrendingDown,
    TrendingUp,
    Zap
} from 'lucide-react'
import { useEffect, useState } from 'react'
import './App.css'

interface ApiResponse {
  message: string
  data?: {
    timestamp: string
    service: string
  }
}

interface StockData {
  symbol: string
  price: number
  change: number
  changePercent: number
  volume: number
}

interface SystemStatus {
  backend: boolean
  database: boolean
  redis: boolean
  mcp: boolean
}

function App() {
  const [apiResponse, setApiResponse] = useState<ApiResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [marketAnalysis, setMarketAnalysis] = useState<any>(null)
  const [portfolioData, setPortfolioData] = useState<any>(null)
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    backend: false,
    database: false,
    redis: false,
    mcp: false
  })

  // 实时股票数据
  const [stockData, setStockData] = useState<StockData[]>([])
  const [dataSource, setDataSource] = useState<string>("")
  const [stocksLoading, setStocksLoading] = useState<boolean>(true)

  const callBackendAPI = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get<ApiResponse>('/api/test')
      setApiResponse(response.data)
      setSystemStatus(prev => ({ ...prev, backend: true }))
    } catch (err) {
      setError('无法连接到后端服务，请确保后端正在运行')
      setSystemStatus(prev => ({ ...prev, backend: false }))
      console.error('API 调用失败:', err)
    } finally {
      setLoading(false)
    }
  }

  const checkSystemHealth = async () => {
    try {
      // 检查后端健康状态
      await axios.get('/health')
      setSystemStatus(prev => ({ ...prev, backend: true }))
      
      // 检查 MCP 状态
      await axios.get('/api/mcp/status')
      setSystemStatus(prev => ({ ...prev, mcp: true }))
      
      // 模拟数据库和 Redis 检查
      setSystemStatus(prev => ({ 
        ...prev, 
        database: true, 
        redis: true 
      }))
    } catch (err) {
      console.error('系统健康检查失败:', err)
    }
  }

  const analyzeStock = async (symbol: string) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post('/api/analyze/stock', null, {
        params: { symbol }
      })
      setAnalysisResult(response.data)
    } catch (err) {
      setError('股票分析失败，请稍后重试')
      console.error('股票分析失败:', err)
    } finally {
      setLoading(false)
    }
  }

  const analyzeMarket = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post('/api/analyze/market', null, {
        params: { timeframe: '1d' }
      })
      setMarketAnalysis(response.data)
    } catch (err) {
      setError('市场分析失败，请稍后重试')
      console.error('市场分析失败:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadPortfolio = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get('/api/portfolio/status')
      setPortfolioData(response.data)
    } catch (err) {
      setError('投资组合加载失败，请稍后重试')
      console.error('投资组合加载失败:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadRealtimeStocks = async () => {
    setStocksLoading(true)
    setError(null)
    try {
      console.log('开始加载股票数据...')
      const response = await axios.get('/api/stocks/realtime')
      console.log('股票数据响应:', response.data)
      
      // 验证响应数据结构
      if (!response.data || !Array.isArray(response.data.stocks)) {
        throw new Error('无效的股票数据格式')
      }
      
      // 转换字段名为驼峰命名，并确保所有数值字段都有默认值
      const stocks = response.data.stocks.map((stock: any) => {
        if (!stock || typeof stock !== 'object') {
          throw new Error('无效的股票数据项')
        }
        return {
          symbol: stock.symbol || '',
          price: Number(stock.price) || 0,
          change: Number(stock.change) || 0,
          changePercent: Number(stock.change_percent) || 0,
          volume: Number(stock.volume) || 0,
          high: Number(stock.high) || 0,
          low: Number(stock.low) || 0,
          open: Number(stock.open) || 0
        }
      })
      
      setStockData(stocks)
      setDataSource(response.data.data_source || '未知')
    } catch (err) {
      console.error('实时股票数据加载失败:', err)
      setError(`实时股票数据加载失败: ${err instanceof Error ? err.message : '未知错误'}`)
      // 如果 API 失败，使用模拟数据
      setStockData([
        { symbol: 'AAPL', price: 175.43, change: 2.15, changePercent: 1.24, volume: 45678900 },
        { symbol: 'GOOGL', price: 142.56, change: -1.23, changePercent: -0.86, volume: 23456700 },
        { symbol: 'MSFT', price: 378.85, change: 3.42, changePercent: 0.91, volume: 34567800 },
        { symbol: 'TSLA', price: 248.12, change: -5.67, changePercent: -2.23, volume: 56789000 },
        { symbol: 'AMZN', price: 155.78, change: 1.89, changePercent: 1.23, volume: 12345600 }
      ])
      setDataSource("模拟数据")
    } finally {
      setStocksLoading(false)
    }
  }

  useEffect(() => {
    callBackendAPI()
    checkSystemHealth()
    loadRealtimeStocks()
  }, [])

  return (
    <div className="app">
      {/* 顶部导航栏 */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <TrendingUp className="logo-icon" />
            <span>Agentic Stock System</span>
          </div>
          <div className="header-actions">
            <button className="refresh-btn" onClick={callBackendAPI} disabled={loading}>
              <RefreshCw className={`refresh-icon ${loading ? 'spinning' : ''}`} />
              刷新数据
            </button>
            <button className="settings-btn">
              <Settings className="settings-icon" />
            </button>
          </div>
        </div>
      </header>

      {/* 主要内容区域 */}
      <main className="main-content">
        {/* 系统状态卡片 */}
        <div className="status-grid">
          <div className="status-card">
            <div className="status-header">
              <Server className="status-icon" />
              <span>后端服务</span>
            </div>
            <div className={`status-indicator ${systemStatus.backend ? 'online' : 'offline'}`}>
              {systemStatus.backend ? <CheckCircle /> : <AlertCircle />}
              {systemStatus.backend ? '在线' : '离线'}
            </div>
          </div>
          
          <div className="status-card">
            <div className="status-header">
              <Database className="status-icon" />
              <span>数据库</span>
            </div>
            <div className={`status-indicator ${systemStatus.database ? 'online' : 'offline'}`}>
              {systemStatus.database ? <CheckCircle /> : <AlertCircle />}
              {systemStatus.database ? '在线' : '离线'}
            </div>
          </div>
          
          <div className="status-card">
            <div className="status-header">
              <Activity className="status-icon" />
              <span>Redis 缓存</span>
            </div>
            <div className={`status-indicator ${systemStatus.redis ? 'online' : 'offline'}`}>
              {systemStatus.redis ? <CheckCircle /> : <AlertCircle />}
              {systemStatus.redis ? '在线' : '离线'}
            </div>
          </div>
          
          <div className="status-card">
            <div className="status-header">
              <Zap className="status-icon" />
              <span>MCP 服务器</span>
            </div>
            <div className={`status-indicator ${systemStatus.mcp ? 'online' : 'offline'}`}>
              {systemStatus.mcp ? <CheckCircle /> : <AlertCircle />}
              {systemStatus.mcp ? '在线' : '离线'}
            </div>
          </div>
        </div>

        {/* 股票数据表格 */}
        <div className="dashboard-section">
          <div className="section-header">
            <h2>实时股票数据</h2>
            <div className="data-source-info">
              <span className="data-source-label">数据源:</span>
              <span className={`data-source-value ${dataSource.includes('Alpha Vantage') ? 'real' : 'simulated'}`}>
                {dataSource || '加载中...'}
              </span>
            </div>
            <div className="section-actions">
              <button 
                className="action-btn primary" 
                onClick={() => analyzeMarket()}
                disabled={loading}
              >
                <BarChart3 className="btn-icon" />
                {loading ? '分析中...' : '市场分析'}
              </button>
              <button 
                className="action-btn secondary"
                onClick={() => loadPortfolio()}
                disabled={loading}
              >
                <Activity className="btn-icon" />
                {loading ? '加载中...' : '投资组合'}
              </button>
            </div>
          </div>
          
          <div className="stock-table-container">
            <table className="stock-table">
              <thead>
                <tr>
                  <th>股票代码</th>
                  <th>当前价格</th>
                  <th>涨跌额</th>
                  <th>涨跌幅</th>
                  <th>成交量</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {stocksLoading ? (
                  <tr>
                    <td colSpan={6} className="loading-cell">
                      <div className="loading-spinner">加载中...</div>
                    </td>
                  </tr>
                ) : stockData.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="empty-cell">
                      暂无数据
                    </td>
                  </tr>
                ) : (
                  stockData.map((stock) => (
                  <tr key={stock.symbol}>
                    <td className="symbol-cell">
                      <span className="symbol">{stock.symbol}</span>
                    </td>
                    <td className="price-cell">
                      <DollarSign className="dollar-icon" />
                      {(stock.price || 0).toFixed(2)}
                    </td>
                    <td className={`change-cell ${(stock.change || 0) >= 0 ? 'positive' : 'negative'}`}>
                      {(stock.change || 0) >= 0 ? <TrendingUp className="trend-icon" /> : <TrendingDown className="trend-icon" />}
                      {(stock.change || 0) >= 0 ? '+' : ''}{(stock.change || 0).toFixed(2)}
                    </td>
                    <td className={`change-percent-cell ${(stock.changePercent || 0) >= 0 ? 'positive' : 'negative'}`}>
                      {(stock.changePercent || 0) >= 0 ? '+' : ''}{(stock.changePercent || 0).toFixed(2)}%
                    </td>
                    <td className="volume-cell">
                      {(stock.volume || 0).toLocaleString()}
                    </td>
                    <td className="action-cell">
                      <button 
                        className="stock-action-btn"
                        onClick={() => analyzeStock(stock.symbol)}
                        disabled={loading}
                      >
                        {loading ? '分析中...' : 'AI分析'}
                      </button>
                    </td>
                  </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* 分析结果显示区域 */}
        {(analysisResult || marketAnalysis || portfolioData) && (
          <div className="analysis-results-section">
            <div className="section-header">
              <h2>AI 分析结果</h2>
            </div>
            
            {analysisResult && (
              <div className="analysis-card">
                <h3>📈 {analysisResult.symbol} 股票分析</h3>
                <div className="analysis-content">
                  <div className="analysis-section">
                    <h4>技术指标</h4>
                    <div className="indicators-grid">
                      <div className="indicator">
                        <span className="indicator-label">RSI:</span>
                        <span className="indicator-value">{analysisResult.analysis.technical_indicators.rsi}</span>
                      </div>
                      <div className="indicator">
                        <span className="indicator-label">MACD:</span>
                        <span className="indicator-value">{analysisResult.analysis.technical_indicators.macd}</span>
                      </div>
                      <div className="indicator">
                        <span className="indicator-label">20日均线:</span>
                        <span className="indicator-value">${analysisResult.analysis.technical_indicators.moving_average_20}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="analysis-section">
                    <h4>AI 洞察</h4>
                    <ul className="insights-list">
                      {analysisResult.analysis.ai_insights.map((insight: string, index: number) => (
                        <li key={index}>{insight}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className="analysis-section">
                    <h4>投资建议</h4>
                    <div className="recommendation">
                      <div className="recommendation-action">
                        <strong>操作建议:</strong> {analysisResult.analysis.recommendation.action}
                      </div>
                      <div className="recommendation-confidence">
                        <strong>置信度:</strong> {(analysisResult.analysis.recommendation.confidence * 100).toFixed(0)}%
                      </div>
                      <div className="recommendation-targets">
                        <span>目标价: ${analysisResult.analysis.recommendation.target_price}</span>
                        <span>止损价: ${analysisResult.analysis.recommendation.stop_loss}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {marketAnalysis && (
              <div className="analysis-card">
                <h3>🌍 市场整体分析</h3>
                <div className="analysis-content">
                  <div className="analysis-section">
                    <h4>市场概况</h4>
                    <div className="market-overview">
                      <div className="market-item">
                        <span className="market-label">整体趋势:</span>
                        <span className="market-value">{marketAnalysis.market_overview.overall_trend}</span>
                      </div>
                      <div className="market-item">
                        <span className="market-label">市场情绪:</span>
                        <span className="market-value">{marketAnalysis.market_overview.market_sentiment}</span>
                      </div>
                      <div className="market-item">
                        <span className="market-label">波动率指数:</span>
                        <span className="market-value">{marketAnalysis.market_overview.volatility_index}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="analysis-section">
                    <h4>AI 市场展望</h4>
                    <p className="market-outlook">{marketAnalysis.ai_analysis.market_outlook}</p>
                  </div>
                  
                  <div className="analysis-section">
                    <h4>投资建议</h4>
                    <div className="strategy-recommendation">
                      <div className="strategy">
                        <strong>策略:</strong> {marketAnalysis.recommendations.strategy}
                      </div>
                      <div className="sector-allocation">
                        <strong>行业配置:</strong>
                        <div className="allocation-grid">
                          {Object.entries(marketAnalysis.recommendations.sector_allocation).map(([sector, allocation]) => (
                            <div key={sector} className="allocation-item">
                              <span>{sector}: {allocation as number}%</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {portfolioData && (
              <div className="analysis-card">
                <h3>💼 投资组合状态</h3>
                <div className="analysis-content">
                  <div className="portfolio-summary">
                    <div className="portfolio-metric">
                      <span className="metric-label">总价值:</span>
                      <span className="metric-value">${portfolioData.total_value.toLocaleString()}</span>
                    </div>
                    <div className="portfolio-metric">
                      <span className="metric-label">总收益:</span>
                      <span className="metric-value positive">+${portfolioData.total_gain.toLocaleString()}</span>
                    </div>
                    <div className="portfolio-metric">
                      <span className="metric-label">收益率:</span>
                      <span className="metric-value positive">+{portfolioData.total_gain_percent.toFixed(2)}%</span>
                    </div>
                  </div>
                  
                  <div className="positions-table">
                    <h4>持仓详情</h4>
                    <table className="portfolio-table">
                      <thead>
                        <tr>
                          <th>股票</th>
                          <th>股数</th>
                          <th>当前价格</th>
                          <th>市值</th>
                          <th>收益</th>
                          <th>权重</th>
                        </tr>
                      </thead>
                      <tbody>
                        {portfolioData.positions.map((position: any, index: number) => (
                          <tr key={index}>
                            <td className="symbol-cell">{position.symbol}</td>
                            <td>{position.shares}</td>
                            <td>${position.current_price.toFixed(2)}</td>
                            <td>${position.value.toLocaleString()}</td>
                            <td className={position.gain >= 0 ? 'positive' : 'negative'}>
                              {position.gain >= 0 ? '+' : ''}${position.gain.toLocaleString()}
                            </td>
                            <td>{position.weight.toFixed(1)}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* API 测试区域 */}
        <div className="api-test-section">
          <div className="section-header">
            <h2>API 连接测试</h2>
          </div>
          
          <div className="api-test-container">
            <div className="api-test-form">
          <button 
            onClick={callBackendAPI}
            disabled={loading}
                className="test-btn"
              >
                {loading ? (
                  <>
                    <RefreshCw className="spinning" />
                    测试中...
                  </>
                ) : (
                  <>
                    <Zap className="btn-icon" />
                    测试后端连接
                  </>
                )}
          </button>
            </div>
          
          {apiResponse && (
            <div className="api-response success">
                <div className="response-header">
                  <CheckCircle className="response-icon" />
                  <span>连接成功</span>
                </div>
                <div className="response-content">
              <p><strong>消息：</strong> {apiResponse.message}</p>
              {apiResponse.data && (
                    <div className="response-details">
                  <p><strong>服务：</strong> {apiResponse.data.service}</p>
                  <p><strong>时间戳：</strong> {apiResponse.data.timestamp}</p>
                </div>
              )}
                </div>
            </div>
          )}
          
          {error && (
            <div className="api-response error">
                <div className="response-header">
                  <AlertCircle className="response-icon" />
                  <span>连接失败</span>
                </div>
                <div className="response-content">
              <p>{error}</p>
                </div>
            </div>
          )}
          </div>
        </div>
      </main>

      {/* 底部信息 */}
      <footer className="footer">
        <div className="footer-content">
          <p>基于 LangGraph 的 AI Agent System | 前端端口：3000 | 后端端口：8000</p>
          <p>Docker 容器化部署 | 实时数据监控</p>
        </div>
      </footer>
    </div>
  )
}

export default App
