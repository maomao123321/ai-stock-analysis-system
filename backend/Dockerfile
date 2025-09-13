# 使用 Python 3.11 官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MCP_SERVER_PORT=8001
ENV MCP_SERVER_HOST=0.0.0.0

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000 8001

# 启动命令 - 同时启动 MCP 服务器和 FastAPI
CMD ["sh", "-c", "python mcp_server.py & uvicorn main:app --host 0.0.0.0 --port 8000"]
