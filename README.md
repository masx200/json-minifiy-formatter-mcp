# JSON 格式化/压缩 MCP 服务器

一个基于 MCP (Model Context Protocol) 的 JSON 格式化与压缩工具服务器，支持将
JSON 字符串格式化为易读的格式或压缩为单行。

## 功能特性

- **JSON 格式化**: 将压缩的 JSON 字符串格式化为带缩进的漂亮格式
- **JSON 压缩**: 将格式化的 JSON 压缩为单行，移除所有空白字符
- **键排序**: 可选择是否对 JSON 键进行排序
- **UTF-8 支持**: 完整支持 Unicode 字符，保留中文字符

## 安装

### 环境要求

- Python 3.8+
- uv (Python 包管理器)

### 安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/masx200/json-minifiy-formatter-mcp.git
cd json-minifiy-formatter-mcp
```

2. 使用 uv 安装依赖：

```bash
uv sync
```

## 配置

### 环境变量

- **HTTP_API_TOKEN** (可选): 为 streamable-http 协议设置 HTTP Bearer 身份验证令牌。如果设置，所有 HTTP 请求必须包含 `Authorization: Bearer <token>` 头部。

### 协议选择

本项目支持两种协议：

- **stdio**: 标准输入输出协议
- **streamable-http**: 流式 HTTP 协议

### Cursor 配置

#### stdio 协议配置

在 Cursor 的 MCP 配置文件中添加以下内容：

```json
{
  "mcpServers": {
    "json-minifiy-formatter-mcp": {
      "name": "JSON 格式化 / 压缩",
      "type": "stdio",
      "description": "JSON 格式化 / 压缩",
      "isActive": true,
      "registryUrl": "https://pypi.tuna.tsinghua.edu.cn/simple",
      "command": "uv",
      "args": [
        "run",
        "D:\\github\\json-minifiy-formatter-mcp\\json_mcp-stdio.py"
      ]
    }
  }
}
```

#### streamable-http 协议配置

**基本配置（无身份验证）：**

```json
{
  "mcpServers": {
    "json-minifiy-formatter-mcp-http": {
      "transport": "streamable-http",
      "name": "JSON 格式化 / 压缩 (HTTP)",
      "type": "http",
      "description": "JSON 格式化 / 压缩 (streamable-http)",
      "isActive": true,
      "url": "http://localhost:6600/mcp"
    }
  }
}
```

**带身份验证的配置（使用HTTP_API_TOKEN）：**

首先设置环境变量：
```bash
export HTTP_API_TOKEN="your-secret-token-here"
```

然后在配置中添加headers：

```json
{
  "mcpServers": {
    "json-minifiy-formatter-mcp-http": {
      "transport": "streamable-http",
      "name": "JSON 格式化 / 压缩 (HTTP)",
      "type": "http",
      "description": "JSON 格式化 / 压缩 (streamable-http)",
      "isActive": true,
      "url": "http://localhost:6600/mcp",
      "headers": {
        "Authorization": "Bearer your-secret-token-here"
      }
    }
  }
}
```

### Claude Desktop 配置

#### stdio 协议配置

在 Claude Desktop 的配置文件中添加：

```json
{
  "mcpServers": {
    "json-formatter": {
      "command": "uv",
      "args": ["run", "/path/to/json-minifiy-formatter-mcp/json_mcp-stdio.py"]
    }
  }
}
```

#### streamable-http 协议配置

**基本配置（无身份验证）：**

```json
{
  "mcpServers": {
    "json-minifiy-formatter-mcp-http": {
      "transport": "streamable-http",
      "name": "JSON 格式化 / 压缩 (HTTP)",
      "type": "http",
      "description": "JSON 格式化 / 压缩 (streamable-http)",
      "isActive": true,
      "url": "http://localhost:6600/mcp"
    }
  }
}
```

**带身份验证的配置（使用HTTP_API_TOKEN）：**

首先设置环境变量：
```bash
export HTTP_API_TOKEN="your-secret-token-here"
```

然后在配置中添加headers：

```json
{
  "mcpServers": {
    "json-minifiy-formatter-mcp-http": {
      "transport": "streamable-http",
      "name": "JSON 格式化 / 压缩 (HTTP)",
      "type": "http",
      "description": "JSON 格式化 / 压缩 (streamable-http)",
      "isActive": true,
      "url": "http://localhost:6600/mcp",
      "headers": {
        "Authorization": "Bearer your-secret-token-here"
      }
    }
  }
}
```

## 使用方法

### 工具 1: format_json - JSON 格式化

将 JSON 字符串格式化为带缩进的漂亮格式。

**参数：**

- `raw` (string, 必需): 原始 JSON 字符串
- `indent` (integer, 可选, 默认值: 2): 缩进空格数
- `sort_keys` (boolean, 可选, 默认值: true): 是否对键排序

**示例：**

```json
{ "name": "张三", "age": 25, "skills": ["Python", "JavaScript"] }
```

**格式化后：**

```json
{
  "age": 25,
  "name": "张三",
  "skills": ["Python", "JavaScript"]
}
```

### 工具 2: minify_json - JSON 压缩

将 JSON 字符串压缩为单行，移除所有空白字符。

**参数：**

- `raw` (string, 必需): 原始 JSON 字符串
- `sort_keys` (boolean, 可选, 默认值: true): 是否对键排序

**示例：**

```json
{
  "name": "张三",
  "age": 25,
  "skills": ["Python", "JavaScript"]
}
```

**压缩后：**

```json
{ "age": 25, "name": "张三", "skills": ["Python", "JavaScript"] }
```

## 开发

### 本地运行

#### stdio 协议

```bash
uv run python json_mcp-stdio.py
```

#### streamable-http 协议

**无身份验证模式：**
```bash
uv run python json_mcp-streamable-http.py
```

**带身份验证模式（设置HTTP_API_TOKEN）：**
```bash
# Linux/macOS
export HTTP_API_TOKEN="your-secret-token-here"
uv run python json_mcp-streamable-http.py

# Windows PowerShell
$env:HTTP_API_TOKEN="your-secret-token-here"
uv run python json_mcp-streamable-http.py

# Windows CMD
set HTTP_API_TOKEN=your-secret-token-here
uv run python json_mcp-streamable-http.py
```

启动后，服务器将在 `http://localhost:6600` 上运行。

### 项目结构

```
json-minifiy-formatter-mcp/
├── json_mcp-stdio.py          # stdio 协议主程序文件
├── json_mcp-streamable-http.py # streamable-http 协议主程序文件
├── pyproject.toml       # 项目配置
├── uv.lock             # 依赖锁定文件
├── README.md           # 项目说明
└── LICENSE             # 许可证
```

### 技术栈

- **Python 3.8+**: 主要编程语言
- **uv**: Python 包管理器
- **mcp**: Model Context Protocol 库
- **asyncio**: 异步编程支持
