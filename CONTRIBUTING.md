# 🤝 Contributing to AI Stock Analysis System

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Issue Guidelines](#issue-guidelines)

## 📜 Code of Conduct

This project follows a code of conduct that we expect all contributors to adhere to. By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Node.js 16.20.2+ (recommended 18+)
- Docker 20.10+
- Docker Compose 2.0+
- Git

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/ai-stock-analysis-system.git
   cd ai-stock-analysis-system
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/maomao123321/ai-stock-analysis-system.git
   ```

4. **Install dependencies**
   ```bash
   # Backend
   docker compose up -d
   
   # Frontend
   cd frontend-vue
   npm install
   ```

5. **Start development servers**
   ```bash
   # Frontend (in one terminal)
   cd frontend-vue
   npm run dev
   
   # Backend is already running via Docker
   ```

## 🔄 Development Process

### Branch Naming

Use descriptive branch names:
- `feature/stock-chart-integration`
- `bugfix/api-error-handling`
- `docs/update-readme`
- `refactor/component-structure`

### Commit Messages

Follow conventional commit format:
```
type(scope): description

feat(frontend): add stock chart visualization
fix(api): resolve 405 method not allowed error
docs(readme): update installation instructions
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 📤 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   # Frontend tests
   cd frontend-vue
   npm run test
   
   # Backend tests
   cd backend
   python -m pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Use the provided PR template
   - Link related issues
   - Add screenshots if applicable

## 📏 Coding Standards

### Frontend (Vue 3 + TypeScript)

- Use TypeScript for type safety
- Follow Vue 3 Composition API patterns
- Use ESLint and Prettier for code formatting
- Write meaningful component names
- Use proper prop validation

```typescript
// Good example
interface StockData {
  symbol: string;
  price: number;
  change: number;
}

const props = defineProps<{
  stockData: StockData;
  isLoading: boolean;
}>();
```

### Backend (FastAPI + Python)

- Follow PEP 8 style guide
- Use type hints
- Write comprehensive docstrings
- Handle errors gracefully

```python
# Good example
from typing import Dict, Any, Optional

async def analyze_stock(symbol: str) -> Dict[str, Any]:
    """
    Analyze a stock symbol and return comprehensive analysis.
    
    Args:
        symbol: Stock symbol to analyze
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        ValueError: If symbol is invalid
    """
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    
    # Implementation here
    return analysis_result
```

## 🐛 Issue Guidelines

### Bug Reports

Use the bug report template and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

### Feature Requests

Use the feature request template and include:
- Problem description
- Proposed solution
- Alternative solutions considered
- Additional context

## 🧪 Testing

### Frontend Testing

```bash
cd frontend-vue
npm run test:unit    # Unit tests
npm run test:e2e     # End-to-end tests
npm run test:coverage # Coverage report
```

### Backend Testing

```bash
cd backend
python -m pytest tests/ -v
python -m pytest --cov=backend tests/
```

## 📚 Documentation

- Update README.md for significant changes
- Add JSDoc comments for complex functions
- Update API documentation for backend changes
- Include code examples in docstrings

## 🔍 Code Review

All submissions require review. Reviewers will check for:
- Code quality and style
- Test coverage
- Documentation updates
- Performance implications
- Security considerations

## 📞 Getting Help

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing issues and PRs

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
