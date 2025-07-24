# JSON 格式化/压缩 MCP 服务器

一个基于 MCP (Model Context Protocol) 的 JSON 格式化与压缩工具服务器，支持将 JSON 字符串格式化为易读的格式或压缩为单行。

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

### Cursor 配置

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
        "D:\\github\\json-minifiy-formatter-mcp\\json_mcp.py"
      ]
    }
  }
}
```

### Claude Desktop 配置

在 Claude Desktop 的配置文件中添加：

```json
{
  "mcpServers": {
    "json-formatter": {
      "command": "uv",
      "args": [
        "run",
        "/path/to/json-minifiy-formatter-mcp/json_mcp.py"
      ]
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
{"name":"张三","age":25,"skills":["Python","JavaScript"]}
```

**格式化后：**
```json
{
  "age": 25,
  "name": "张三",
  "skills": [
    "Python",
    "JavaScript"
  ]
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
  "skills": [
    "Python",
    "JavaScript"
  ]
}
```

**压缩后：**
```json
{"age":25,"name":"张三","skills":["Python","JavaScript"]}
```

## 开发

### 本地运行

```bash
uv run python json_mcp.py
```

### 项目结构

```
json-minifiy-formatter-mcp/
├── json_mcp.py          # 主程序文件
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

## 贡献

欢迎提交 Issue 和 Pull Request！
