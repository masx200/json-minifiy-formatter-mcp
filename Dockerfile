FROM python:3.13-slim

# 设置工作目录
WORKDIR /app
run pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
run  pip config set install.trusted-host 'https://pypi.tuna.tsinghua.edu.cn'
# 安装uv包管理器
RUN pip install uv

# 复制项目文件
COPY pyproject.toml uv.lock ./
COPY json_mcp-streamable-http.py ./


copy ./* /app

# 安装依赖
RUN uv sync --frozen

# 暴露端口（根据应用需要）
EXPOSE 6600

# 使用指定的启动命令
CMD ["uv", "run", "python", "json_mcp-streamable-http.py"]