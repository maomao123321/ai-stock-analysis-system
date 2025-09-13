# 🚀 AI 股票分析系统

基于 Vue 3 + Vite + FastAPI 的智能股票分析系统，集成多个 AI Agent 进行协作分析。

## ✨ 功能特性

- 🔍 **股票代码输入**：支持输入任何股票代码进行分析
- 🤖 **AI Agent 协作**：多个 AI Agent 协同工作，提供全面分析
- 📊 **技术指标分析**：RSI、MACD、移动平均线等技术指标
- 📈 **趋势分析**：短期、中期、长期趋势分析
- ⚠️ **风险评估**：波动率、风险等级、Beta 值评估
- 💡 **投资建议**：操作建议、置信度、目标价、止损价
- 📱 **响应式设计**：现代化的用户界面，支持各种设备

## 🛠️ 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite 4.5.3** - 快速的前端构建工具
- **TypeScript 4.9.5** - 类型安全的 JavaScript
- **Axios** - HTTP 客户端
- **Vue Router** - 官方路由管理器

### 后端
- **FastAPI** - 现代、快速的 Python Web 框架
- **PostgreSQL** - 关系型数据库
- **Redis** - 内存数据库，用于缓存
- **Docker** - 容器化部署
- **Alpha Vantage API** - 股票数据源

## 🚀 快速开始

### 环境要求

- **Node.js**: 16.20.2+ (推荐 18+)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### 安装步骤

1. **克隆仓库**
```bash
git clone <your-repo-url>
cd stock-agent
```

2. **启动后端服务**
```bash
docker compose up -d
```

3. **安装前端依赖**
```bash
cd frontend-vue
npm install
```

4. **启动前端服务**
```bash
npm run dev
```

5. **访问应用**
- 前端：http://localhost:3001
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 📖 使用指南

1. 在输入框中输入股票代码（如：AAPL、GOOGL、MSFT）
2. 点击"开始分析"按钮
3. 查看 AI Agent 协作分析结果：
   - 实时股价数据
   - 技术指标分析
   - 趋势分析
   - 风险评估
   - 投资建议

## 🔧 开发指南

### 项目结构

```
stock-agent/
├── frontend-vue/          # Vue 前端
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── router/        # 路由配置
│   │   └── assets/        # 静态资源
│   ├── package.json
│   └── vite.config.ts
├── backend/               # FastAPI 后端
│   ├── main.py           # 主应用
│   ├── agents/           # AI Agent 实现
│   └── requirements.txt
├── docker-compose.yml    # Docker 配置
└── README.md
```

### 开发命令

```bash
# 前端开发
cd frontend-vue
npm run dev          # 启动开发服务器
npm run build        # 构建生产版本
npm run preview      # 预览构建结果

# 后端开发
cd backend
python main.py       # 直接运行（需要配置环境变量）
```

## ⚠️ 常见问题与解决方案

### 1. Node.js 版本兼容性问题

**问题**：`TypeError: crypto$2.getRandomValues is not a function`

**原因**：Vite 5.x 和 TypeScript 5.x 需要 Node.js 18+，但环境是 Node.js 16.20.2

**解决方案**：
```bash
# 降级到兼容版本
npm install vite@^4.5.3 typescript@~4.9.5 --save-dev
```

**避免方法**：检查 Node.js 版本要求，或升级到 Node.js 18+

### 2. Docker 端口占用问题

**问题**：前端无法在默认端口 3000 启动

**原因**：Docker Compose 中的前端服务占用了 3000 端口

**解决方案**：Vite 自动切换到 3001 端口

**避免方法**：统一端口规划，或修改 Docker Compose 配置

### 3. 前后端连接问题

**问题**：`Error: getaddrinfo ENOTFOUND backend`

**原因**：Vite 代理配置使用 `http://backend:8000`，这在 Docker 网络外无法解析

**解决方案**：
```typescript
// vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 改为 localhost
        changeOrigin: true
      }
    }
  }
})
```

**避免方法**：区分开发环境（localhost）和生产环境（Docker 服务名）

### 4. HTTP 方法不匹配

**问题**：`405 Method Not Allowed`

**原因**：前端用 `GET` 请求，后端 API 是 `POST` 方法

**解决方案**：
```javascript
// 统一使用 POST 方法
const response = await axios.post(`/api/analyze/stock?symbol=${symbol}`)
```

**避免方法**：API 设计时明确文档化 HTTP 方法

### 5. 数据类型转换问题

**问题**：`toFixed is not a function`

**原因**：后端返回的 `change_percent` 是字符串，前端直接调用 `toFixed()`

**解决方案**：
```javascript
// 安全的数值处理
const price = Number(value || 0).toFixed(2)
const changePercent = Number(value || 0) >= 0 ? 'positive' : 'negative'
```

**避免方法**：前后端统一数据类型，或前端做类型检查

### 6. API 密钥配置问题

**问题**：`无法获取股票数据: Unknown error`

**原因**：Alpha Vantage API 密钥无效或 API 限制

**解决方案**：添加模拟数据作为备选方案

**避免方法**：API 密钥管理，添加降级策略

### 7. Vue 路由配置问题

**问题**：页面显示空白或默认 Vite 页面

**原因**：内容放在 `App.vue` 但路由指向 `HomeView.vue`

**解决方案**：将内容移到正确的路由组件

**避免方法**：理解 Vue Router 的工作原理

## 🎯 最佳实践

### 开发环境设置

```bash
# 1. 检查 Node.js 版本
node --version  # 建议 18+

# 2. 检查端口占用
lsof -i :3000
lsof -i :8000

# 3. 启动顺序
docker compose up -d  # 先启动后端
npm run dev          # 再启动前端
```

### API 设计规范

```javascript
// 明确 HTTP 方法
POST /api/analyze/stock  // 不是 GET

// 统一数据格式
{
  "price": 215.0,           // 数字类型
  "change_percent": "-0.5"  // 字符串类型，需要转换
}
```

### 前端类型安全

```javascript
// 安全的数值处理
const price = Number(value || 0).toFixed(2)
const changePercent = Number(value || 0) >= 0 ? 'positive' : 'negative'
```

### 错误处理策略

```javascript
// API 降级策略
if (apiError) {
  useSimulatedData()
  showWarning("使用模拟数据")
}
```

## 🔑 环境变量配置

创建 `.env` 文件：

```env
# Alpha Vantage API
ALPHA_VANTAGE_API_KEY=your_api_key_here

# OpenAI API
OPENAI_API_KEY=your_openai_key_here

# 数据库
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/agentic_stock_db
REDIS_URL=redis://localhost:6379
```

## 📊 API 接口

### 股票分析

```http
POST /api/analyze/stock?symbol=AAPL
Content-Type: application/json
```

**响应示例**：
```json
{
  "symbol": "AAPL",
  "real_time_data": {
    "price": 215.0,
    "change": -5,
    "change_percent": "-0.5",
    "volume": 4223765
  },
  "analysis": {
    "technical_indicators": {
      "rsi": 49.0,
      "macd": "negative"
    },
    "recommendation": {
      "action": "持有观望",
      "confidence": 0.6,
      "target_price": 236.5
    }
  }
}
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代、快速的 Python Web 框架
- [Alpha Vantage](https://www.alphavantage.co/) - 股票数据 API
- [Vite](https://vitejs.dev/) - 快速的前端构建工具

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/your-username/stock-agent/issues)
- 发送邮件至：your-email@example.com

---

⭐ 如果这个项目对你有帮助，请给它一个星标！