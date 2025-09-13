<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">📈</span>
          <span>Agentic Stock System</span>
        </div>
        <div class="header-actions">
          <button class="refresh-btn" @click="refreshData" :disabled="loading">
            <span class="refresh-icon" :class="{ spinning: loading }">🔄</span>
            刷新数据
          </button>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 系统状态卡片 -->
      <div class="status-grid">
        <div class="status-card">
          <div class="status-header">
            <span class="status-icon">🖥️</span>
            <span>后端服务</span>
          </div>
          <div class="status-indicator" :class="systemStatus.backend ? 'online' : 'offline'">
            <span>{{ systemStatus.backend ? '✅' : '❌' }}</span>
            {{ systemStatus.backend ? '在线' : '离线' }}
          </div>
        </div>
      </div>

      <!-- 股票分析输入区域 -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>AI 股票分析系统</h2>
          <div class="data-source-info">
            <span class="data-source-label">数据源:</span>
            <span class="data-source-value" :class="dataSource.includes('Alpha Vantage') ? 'real' : 'simulated'">
              {{ dataSource || '加载中...' }}
            </span>
          </div>
        </div>
        
        <!-- 股票代码输入区域 -->
        <div class="stock-input-section">
          <div class="input-container">
            <div class="input-group">
              <label for="stockSymbol" class="input-label">请输入股票代码</label>
              <div class="input-wrapper">
                <input 
                  id="stockSymbol"
                  v-model="stockSymbol"
                  type="text" 
                  placeholder="例如: AAPL, GOOGL, MSFT..."
                  class="stock-input"
                  :disabled="analysisLoading"
                  @keyup.enter="analyzeStock"
                />
                <button 
                  @click="analyzeStock"
                  :disabled="!stockSymbol.trim() || analysisLoading"
                  class="analyze-btn"
                >
                  <span v-if="analysisLoading" class="btn-icon spinning">⏳</span>
                  <span v-else class="btn-icon">🔍</span>
                  {{ analysisLoading ? '分析中...' : '开始分析' }}
                </button>
              </div>
              <div class="input-hint">
                <span class="hint-icon">💡</span>
                支持美股代码，如 AAPL、GOOGL、MSFT、TSLA 等
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI 分析结果展示区域 -->
      <div v-if="analysisResult" class="analysis-section">
        <div class="section-header">
          <h2>AI Agent 协作分析结果</h2>
          <div class="analysis-meta">
            <span class="analysis-symbol">{{ analysisResult.symbol }}</span>
            <span class="analysis-time">{{ formatTime(analysisResult.timestamp) }}</span>
          </div>
        </div>
        
        <div class="analysis-content">
          <!-- 分析概览 -->
          <div class="analysis-overview">
            <div class="overview-card">
              <div class="overview-header">
                <span class="overview-icon">📊</span>
                <span>分析概览</span>
              </div>
              <div class="overview-content">
                <div class="overview-item">
                  <span class="overview-label">当前价格:</span>
                  <span class="overview-value price">{{ formatPrice(analysisResult.real_time_data?.price) }}</span>
                </div>
                <div class="overview-item">
                  <span class="overview-label">涨跌幅:</span>
                  <span class="overview-value" :class="Number(analysisResult.real_time_data?.change_percent || 0) >= 0 ? 'positive' : 'negative'">
                    {{ Number(analysisResult.real_time_data?.change_percent || 0) >= 0 ? '+' : '' }}{{ Number(analysisResult.real_time_data?.change_percent || 0).toFixed(2) }}%
                  </span>
                </div>
                <div class="overview-item">
                  <span class="overview-label">成交量:</span>
                  <span class="overview-value">{{ formatVolume(analysisResult.real_time_data?.volume) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- AI 洞察 -->
          <div v-if="analysisResult.analysis?.ai_insights" class="analysis-summary">
            <div class="summary-card">
              <div class="summary-header">
                <span class="summary-icon">🤖</span>
                <span>AI Agent 协作洞察</span>
              </div>
              <div class="summary-content">
                <div class="summary-text">{{ analysisResult.analysis.ai_insights }}</div>
              </div>
            </div>
          </div>

          <!-- 技术指标 -->
          <div v-if="analysisResult.analysis?.technical_indicators" class="detailed-analysis">
            <div class="analysis-card">
              <div class="analysis-header">
                <span class="analysis-icon">📈</span>
                <span>技术指标分析</span>
              </div>
              <div class="analysis-body">
                <div class="analysis-item" v-for="(value, key) in analysisResult.analysis.technical_indicators" :key="key">
                  <div class="analysis-title">{{ key }}</div>
                  <div class="analysis-description">{{ value }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 趋势分析 -->
          <div v-if="analysisResult.analysis?.trend_analysis" class="trend-analysis">
            <div class="analysis-card">
              <div class="analysis-header">
                <span class="analysis-icon">📊</span>
                <span>趋势分析</span>
              </div>
              <div class="analysis-body">
                <div class="analysis-item">
                  <div class="analysis-title">短期趋势</div>
                  <div class="analysis-description">{{ analysisResult.analysis.trend_analysis.short_term }}</div>
                </div>
                <div class="analysis-item">
                  <div class="analysis-title">中期趋势</div>
                  <div class="analysis-description">{{ analysisResult.analysis.trend_analysis.medium_term }}</div>
                </div>
                <div class="analysis-item">
                  <div class="analysis-title">长期趋势</div>
                  <div class="analysis-description">{{ analysisResult.analysis.trend_analysis.long_term }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 风险评估 -->
          <div v-if="analysisResult.analysis?.risk_assessment" class="risk-analysis">
            <div class="analysis-card">
              <div class="analysis-header">
                <span class="analysis-icon">⚠️</span>
                <span>风险评估</span>
              </div>
              <div class="analysis-body">
                <div class="analysis-item">
                  <div class="analysis-title">波动性</div>
                  <div class="analysis-description">{{ analysisResult.analysis.risk_assessment.volatility }}</div>
                </div>
                <div class="analysis-item">
                  <div class="analysis-title">风险等级</div>
                  <div class="analysis-description">{{ analysisResult.analysis.risk_assessment.risk_level }}</div>
                </div>
                <div class="analysis-item">
                  <div class="analysis-title">Beta 值</div>
                  <div class="analysis-description">{{ analysisResult.analysis.risk_assessment.beta }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 投资建议 -->
          <div v-if="analysisResult.analysis?.recommendation" class="recommendation-section">
            <div class="recommendation-card">
              <div class="recommendation-header">
                <span class="recommendation-icon">💡</span>
                <span>投资建议</span>
              </div>
              <div class="recommendation-content">
                <div class="recommendation-item">
                  <div class="recommendation-title">建议操作</div>
                  <div class="recommendation-text">{{ analysisResult.analysis.recommendation.action }}</div>
                </div>
                <div class="recommendation-item">
                  <div class="recommendation-title">置信度</div>
                  <div class="recommendation-text">{{ (analysisResult.analysis.recommendation.confidence * 100).toFixed(0) }}%</div>
                </div>
                <div class="recommendation-item">
                  <div class="recommendation-title">目标价格</div>
                  <div class="recommendation-text">${{ analysisResult.analysis.recommendation.target_price }}</div>
                </div>
                <div class="recommendation-item">
                  <div class="recommendation-title">止损价格</div>
                  <div class="recommendation-text">${{ analysisResult.analysis.recommendation.stop_loss }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 股票数据表格 -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>实时股票数据</h2>
        </div>
        
        <div class="stock-table-container">
          <table class="stock-table">
            <thead>
              <tr>
                <th>股票代码</th>
                <th>当前价格</th>
                <th>涨跌额</th>
                <th>涨跌幅</th>
                <th>成交量</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="stocksLoading">
                <td colspan="5" class="loading-cell">
                  <div class="loading-spinner">加载中...</div>
                </td>
              </tr>
              <tr v-else-if="stockData.length === 0">
                <td colspan="5" class="empty-cell">
                  暂无数据
                </td>
              </tr>
              <tr v-else v-for="stock in stockData" :key="stock.symbol">
                <td class="symbol-cell">
                  <span class="symbol">{{ stock.symbol }}</span>
                </td>
                <td class="price-cell">
                  <span class="dollar-icon">💰</span>
                  {{ Number(stock.price || 0).toFixed(2) }}
                </td>
                <td class="change-cell" :class="Number(stock.change || 0) >= 0 ? 'positive' : 'negative'">
                  <span class="trend-icon">{{ Number(stock.change || 0) >= 0 ? '📈' : '📉' }}</span>
                  {{ Number(stock.change || 0) >= 0 ? '+' : '' }}{{ Number(stock.change || 0).toFixed(2) }}
                </td>
                <td class="change-percent-cell" :class="Number(stock.changePercent || 0) >= 0 ? 'positive' : 'negative'">
                  {{ Number(stock.changePercent || 0) >= 0 ? '+' : '' }}{{ Number(stock.changePercent || 0).toFixed(2) }}%
                </td>
                <td class="volume-cell">
                  {{ (stock.volume || 0).toLocaleString() }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- API 测试区域 -->
      <div class="api-test-section">
        <div class="section-header">
          <h2>API 连接测试</h2>
        </div>
        
        <div class="api-test-container">
          <div class="api-test-form">
            <button 
              @click="testBackendAPI"
              :disabled="loading"
              class="test-btn"
            >
              <span class="btn-icon" :class="{ spinning: loading }">⚡</span>
              {{ loading ? '测试中...' : '测试后端连接' }}
            </button>
          </div>
          
          <div v-if="apiResponse" class="api-response success">
            <div class="response-header">
              <span class="response-icon">✅</span>
              <span>连接成功</span>
            </div>
            <div class="response-content">
              <p><strong>消息：</strong> {{ apiResponse.message }}</p>
              <div v-if="apiResponse.data" class="response-details">
                <p><strong>服务：</strong> {{ apiResponse.data.service }}</p>
                <p><strong>时间戳：</strong> {{ apiResponse.data.timestamp }}</p>
              </div>
            </div>
          </div>
          
          <div v-if="error" class="api-response error">
            <div class="response-header">
              <span class="response-icon">❌</span>
              <span>连接失败</span>
            </div>
            <div class="response-content">
              <p>{{ error }}</p>
            </div>
          </div>
        </div>
      </div>
  </main>

    <!-- 底部信息 -->
    <footer class="footer">
      <div class="footer-content">
        <p>基于 LangGraph 的 AI Agent System | 前端端口：3001 | 后端端口：8000</p>
        <p>Docker 容器化部署 | 实时数据监控</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'

// 响应式数据
const apiResponse = ref(null)
const loading = ref(false)
const error = ref('')
const systemStatus = ref({
  backend: false,
  database: false,
  redis: false,
  mcp: false
})

// 股票数据
const stockData = ref([])
const dataSource = ref('')
const stocksLoading = ref(true)

// 股票分析相关
const stockSymbol = ref('')
const analysisResult = ref(null)
const analysisLoading = ref(false)

// API 调用函数
const testBackendAPI = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await axios.get('/api/test')
    apiResponse.value = response.data
    systemStatus.value.backend = true
  } catch (err) {
    error.value = '无法连接到后端服务，请确保后端正在运行'
    systemStatus.value.backend = false
    console.error('API 调用失败:', err)
  } finally {
    loading.value = false
  }
}

const loadRealtimeStocks = async () => {
  stocksLoading.value = true
  error.value = ''
  try {
    console.log('开始加载股票数据...')
    const response = await axios.get('/api/stocks/realtime')
    console.log('股票数据响应:', response.data)
    
    // 转换字段名为驼峰命名，并确保所有数值字段都有默认值
    const stocks = response.data.stocks.map((stock) => ({
      symbol: stock.symbol || '',
      price: Number(stock.price) || 0,
      change: Number(stock.change) || 0,
      changePercent: Number(stock.change_percent) || 0,
      volume: Number(stock.volume) || 0
    }))
    
    stockData.value = stocks
    dataSource.value = response.data.data_source || '未知'
  } catch (err) {
    console.error('实时股票数据加载失败:', err)
    error.value = `实时股票数据加载失败: ${err instanceof Error ? err.message : '未知错误'}`
    // 如果 API 失败，使用模拟数据
    stockData.value = [
      { symbol: 'AAPL', price: 175.43, change: 2.15, changePercent: 1.24, volume: 45678900 },
      { symbol: 'GOOGL', price: 142.56, change: -1.23, changePercent: -0.86, volume: 23456700 },
      { symbol: 'MSFT', price: 378.85, change: 3.42, changePercent: 0.91, volume: 34567800 },
      { symbol: 'TSLA', price: 248.12, change: -5.67, changePercent: -2.23, volume: 56789000 },
      { symbol: 'AMZN', price: 155.78, change: 1.89, changePercent: 1.23, volume: 12345600 }
    ]
    dataSource.value = "模拟数据"
  } finally {
    stocksLoading.value = false
  }
}

// 股票分析函数
const analyzeStock = async () => {
  if (!stockSymbol.value.trim()) return
  
  analysisLoading.value = true
  error.value = ''
  
  try {
    console.log('开始分析股票:', stockSymbol.value)
    const response = await axios.post('/api/analyze/stock', null, {
      params: { symbol: stockSymbol.value.toUpperCase() }
    })
    console.log('股票分析响应:', response.data)
    
    analysisResult.value = response.data
  } catch (err) {
    console.error('股票分析失败:', err)
    error.value = `股票分析失败: ${err instanceof Error ? err.message : '未知错误'}`
    analysisResult.value = null
  } finally {
    analysisLoading.value = false
  }
}

// 格式化函数
const formatPrice = (price) => {
  return `$${Number(price || 0).toFixed(2)}`
}

const formatVolume = (volume) => {
  return (volume || 0).toLocaleString()
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN')
}

const refreshData = () => {
  testBackendAPI()
  loadRealtimeStocks()
}

// 组件挂载时执行
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #1e293b;
  line-height: 1.6;
}

/* 顶部导航栏 */
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.logo-icon {
  font-size: 2rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #3b82f6;
  color: white;
}

.refresh-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
}

.refresh-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

/* 系统状态网格 */
.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.status-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.status-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
}

.status-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #374151;
}

.status-icon {
  font-size: 1.25rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.status-indicator.online {
  background: #dcfce7;
  color: #166534;
}

.status-indicator.offline {
  background: #fef2f2;
  color: #dc2626;
}

/* 仪表板区域 */
.dashboard-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.data-source-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.data-source-label {
  color: #6b7280;
  font-weight: 500;
}

.data-source-value {
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.75rem;
}

.data-source-value.real {
  background: #dcfce7;
  color: #166534;
}

.data-source-value.simulated {
  background: #fef3c7;
  color: #92400e;
}

.loading-cell, .empty-cell {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.loading-spinner {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.loading-spinner::before {
  content: '';
  width: 1rem;
  height: 1rem;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 股票表格 */
.stock-table-container {
  overflow-x: auto;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
}

.stock-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.stock-table th {
  background: #f8fafc;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e2e8f0;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stock-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.875rem;
}

.stock-table tbody tr:hover {
  background: #f8fafc;
}

.symbol-cell {
  font-weight: 600;
  color: #1e293b;
}

.symbol {
  background: #3b82f6;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.price-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #1e293b;
}

.dollar-icon {
  font-size: 1rem;
}

.change-cell, .change-percent-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

.change-cell.positive, .change-percent-cell.positive {
  color: #059669;
}

.change-cell.negative, .change-percent-cell.negative {
  color: #dc2626;
}

.trend-icon {
  font-size: 1rem;
}

.volume-cell {
  color: #6b7280;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
}

/* 股票输入区域 */
.stock-input-section {
  margin-bottom: 2rem;
}

.input-container {
  max-width: 600px;
  margin: 0 auto;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-label {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  text-align: center;
}

.input-wrapper {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.stock-input {
  flex: 1;
  padding: 1rem 1.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  color: #1e293b;
  background: white;
  transition: all 0.2s ease;
}

.stock-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.stock-input:disabled {
  background: #f8fafc;
  color: #94a3b8;
  cursor: not-allowed;
}

.analyze-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3);
  white-space: nowrap;
}

.analyze-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgba(16, 185, 129, 0.4);
}

.analyze-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
  color: #6b7280;
  font-size: 0.875rem;
  font-style: italic;
}

.hint-icon {
  font-size: 1rem;
}

/* 分析结果区域 */
.analysis-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.analysis-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
}

.analysis-symbol {
  background: #3b82f6;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}

.analysis-time {
  color: #6b7280;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 分析概览 */
.analysis-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.overview-card {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
}

.overview-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #374151;
}

.overview-icon {
  font-size: 1.25rem;
}

.overview-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.overview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.overview-item:last-child {
  border-bottom: none;
}

.overview-label {
  color: #6b7280;
  font-weight: 500;
}

.overview-value {
  font-weight: 600;
  color: #1e293b;
}

.overview-value.price {
  color: #059669;
  font-size: 1.125rem;
}

.overview-value.positive {
  color: #059669;
}

.overview-value.negative {
  color: #dc2626;
}

/* 分析摘要 */
.analysis-summary {
  margin-top: 1rem;
}

.summary-card {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid #bae6fd;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #0c4a6e;
}

.summary-icon {
  font-size: 1.25rem;
}

.summary-text {
  color: #0c4a6e;
  line-height: 1.6;
  font-size: 1rem;
}

/* 详细分析 */
.detailed-analysis {
  margin-top: 1rem;
}

.analysis-card {
  background: #fefce8;
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid #fde047;
}

.analysis-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #713f12;
}

.analysis-icon {
  font-size: 1.25rem;
}

.analysis-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.analysis-item {
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.analysis-title {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.analysis-description {
  color: #6b7280;
  line-height: 1.5;
}

/* 趋势分析 */
.trend-analysis {
  margin-top: 1rem;
}

/* 风险评估 */
.risk-analysis {
  margin-top: 1rem;
}

/* 投资建议 */
.recommendation-section {
  margin-top: 1rem;
}

.recommendation-card {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid #bbf7d0;
}

.recommendation-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #166534;
}

.recommendation-icon {
  font-size: 1.25rem;
}

.recommendation-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.recommendation-item {
  background: white;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #bbf7d0;
}

.recommendation-title {
  font-weight: 600;
  color: #166534;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.recommendation-text {
  color: #166534;
  line-height: 1.6;
  font-size: 1rem;
  font-weight: 500;
}

/* API 测试区域 */
.api-test-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.api-test-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.api-test-form {
  display: flex;
  justify-content: center;
}

.test-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
}

.test-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -3px rgba(59, 130, 246, 0.4);
}

.test-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.spinning {
  animation: spin 1s linear infinite;
}

/* API 响应样式 */
.api-response {
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid;
}

.api-response.success {
  background: #f0fdf4;
  border-color: #bbf7d0;
  color: #166534;
}

.api-response.error {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.response-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-weight: 600;
  font-size: 1.125rem;
}

.response-icon {
  font-size: 1.25rem;
}

.response-content {
  font-size: 0.875rem;
  line-height: 1.6;
}

.response-content p {
  margin-bottom: 0.5rem;
}

.response-details {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

/* 底部信息 */
.footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1.5rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
  color: #64748b;
  font-size: 0.875rem;
}

.footer-content p {
  margin-bottom: 0.5rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .status-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .stock-table-container {
    font-size: 0.75rem;
  }
  
  .stock-table th,
  .stock-table td {
    padding: 0.75rem 0.5rem;
  }
}

@media (max-width: 480px) {
  .logo {
    font-size: 1.25rem;
  }
  
  .logo-icon {
    font-size: 1.5rem;
  }
  
  .test-btn {
    padding: 0.75rem 1.5rem;
    font-size: 0.875rem;
  }
}
</style>
