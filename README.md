# 🚀 AI Stock Analysis System

An intelligent stock analysis system built with Vue 3 + Vite + FastAPI, featuring collaborative AI agents for comprehensive market analysis.

## ✨ Features

- 🔍 **Stock Symbol Input**: Analyze any stock symbol with real-time data
- 🤖 **AI Agent Collaboration**: Multiple AI agents working together for comprehensive analysis
- 📊 **Technical Indicators**: RSI, MACD, Moving Averages, and more
- 📈 **Trend Analysis**: Short-term, medium-term, and long-term trend insights
- ⚠️ **Risk Assessment**: Volatility analysis, risk levels, and Beta evaluation
- 💡 **Investment Recommendations**: Action suggestions, confidence levels, target prices, and stop-loss points
- 📱 **Responsive Design**: Modern UI that works on all devices

## 🛠️ Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite 4.5.3** - Fast frontend build tool
- **TypeScript 4.9.5** - Type-safe JavaScript
- **Axios** - HTTP client
- **Vue Router** - Official router

### Backend
- **Langchain** - Multi-agent system
- **FastAPI** - Modern, fast Python web framework
- **PostgreSQL** - Relational database
- **Redis** - In-memory database for caching
- **Docker** - Containerized deployment
- **Alpha Vantage API** - Stock data source

## 🚀 Quick Start

### Prerequisites

- **Node.js**: 16.20.2+ (recommended 18+)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd stock-agent
```

2. **Start backend services**
```bash
docker compose up -d
```

3. **Install frontend dependencies**
```bash
cd frontend-vue
npm install
```

4. **Start frontend development server**
```bash
npm run dev
```

5. **Access the application**
- Frontend: http://localhost:3001
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📖 Usage Guide

1. Enter a stock symbol in the input field (e.g., AAPL, GOOGL, MSFT)
2. Click "开始分析" (Start Analysis) button
3. View comprehensive AI agent analysis results:
   - Real-time stock data
   - Technical indicator analysis
   - Trend analysis
   - Risk assessment
   - Investment recommendations

## 🔧 Development Guide

### Project Structure

```
stock-agent/
├── frontend-vue/          # Vue frontend
│   ├── src/
│   │   ├── views/         # Page components
│   │   ├── router/        # Router configuration
│   │   └── assets/        # Static assets
│   ├── package.json
│   └── vite.config.ts
├── backend/               # FastAPI backend
│   ├── main.py           # Main application
│   ├── agents/           # AI Agent implementations
│   └── requirements.txt
├── docker-compose.yml    # Docker configuration
└── README.md
```

### Development Commands

```bash
# Frontend development
cd frontend-vue
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview build

# Backend development
cd backend
python main.py       # Run directly (requires env vars)
```

## ⚠️ Common Issues & Solutions

### 1. Node.js Version Compatibility

**Issue**: `TypeError: crypto$2.getRandomValues is not a function`

**Cause**: Vite 5.x and TypeScript 5.x require Node.js 18+, but environment is Node.js 16.20.2

**Solution**:
```bash
# Downgrade to compatible versions
npm install vite@^4.5.3 typescript@~4.9.5 --save-dev
```

**Prevention**: Check Node.js version requirements or upgrade to Node.js 18+

### 2. Docker Port Conflicts

**Issue**: Frontend cannot start on default port 3000

**Cause**: Docker Compose frontend service occupies port 3000

**Solution**: Vite automatically switches to port 3001

**Prevention**: Plan port usage or modify Docker Compose configuration

### 3. Frontend-Backend Connection Issues

**Issue**: `Error: getaddrinfo ENOTFOUND backend`

**Cause**: Vite proxy uses `http://backend:8000`, which cannot be resolved outside Docker network

**Solution**:
```typescript
// vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Change to localhost
        changeOrigin: true
      }
    }
  }
})
```

**Prevention**: Distinguish between development (localhost) and production (Docker service names)

### 4. HTTP Method Mismatch

**Issue**: `405 Method Not Allowed`

**Cause**: Frontend uses GET request, backend API expects POST method

**Solution**:
```javascript
// Use POST method consistently
const response = await axios.post(`/api/analyze/stock?symbol=${symbol}`)
```

**Prevention**: Document HTTP methods clearly in API design

### 5. Data Type Conversion Issues

**Issue**: `toFixed is not a function`

**Cause**: Backend returns `change_percent` as string, frontend calls `toFixed()` directly

**Solution**:
```javascript
// Safe numeric processing
const price = Number(value || 0).toFixed(2)
const changePercent = Number(value || 0) >= 0 ? 'positive' : 'negative'
```

**Prevention**: Ensure consistent data types between frontend and backend, or add type checking

### 6. API Key Configuration Issues

**Issue**: `Unable to get stock data: Unknown error`

**Cause**: Alpha Vantage API key invalid or API limits

**Solution**: Added simulated data as fallback option

**Prevention**: Proper API key management and fallback strategies

### 7. Vue Router Configuration Issues

**Issue**: Blank page or default Vite page displayed

**Cause**: Content placed in `App.vue` but router points to `HomeView.vue`

**Solution**: Move content to correct route component

**Prevention**: Understand Vue Router component mapping

## 🎯 Best Practices

### Development Environment Setup

```bash
# 1. Check Node.js version
node --version  # Recommended 18+

# 2. Check port usage
lsof -i :3000
lsof -i :8000

# 3. Startup sequence
docker compose up -d  # Start backend first
npm run dev          # Then start frontend
```

### API Design Standards

```javascript
// Clear HTTP methods
POST /api/analyze/stock  // Not GET

// Consistent data formats
{
  "price": 215.0,           // Number type
  "change_percent": "-0.5"  // String type, needs conversion
}
```

### Frontend Type Safety

```javascript
// Safe numeric processing
const price = Number(value || 0).toFixed(2)
const changePercent = Number(value || 0) >= 0 ? 'positive' : 'negative'
```

### Error Handling Strategy

```javascript
// API fallback strategy
if (apiError) {
  useSimulatedData()
  showWarning("Using simulated data")
}
```

## 🔑 Environment Variables

Create `.env` file:

```env
# Alpha Vantage API
ALPHA_VANTAGE_API_KEY=your_api_key_here

# OpenAI API
OPENAI_API_KEY=your_openai_key_here

# Database
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/agentic_stock_db
REDIS_URL=redis://localhost:6379
```

## 📊 API Endpoints

### Stock Analysis

```http
POST /api/analyze/stock?symbol=AAPL
Content-Type: application/json
```

**Response Example**:
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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [Vue.js](https://vuejs.org/) - Progressive JavaScript framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast Python web framework
- [Alpha Vantage](https://www.alphavantage.co/) - Stock data API
- [Vite](https://vitejs.dev/) - Fast frontend build tool

## 📞 Contact

For questions or suggestions, please contact:

- Open an [Issue](https://github.com/your-username/stock-agent/issues)
- Send email to: your-email@example.com

---

⭐ If this project helps you, please give it a star!

---

## 中文版本

[查看中文版 README](README_CN.md)
