#!/usr/bin/env python3
"""
MCP server: JSON 格式化 / 压缩
协议：streamable-http
工具：
  - format_json(raw:str, indent:int=2, sort_keys:bool=True) -> str
  - minify_json(raw:str, sort_keys:bool=True) -> str
"""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("json-tools",port=6600)


@mcp.tool()
async def format_json(raw: str, indent: int = 2, sort_keys: bool = True) -> str:
    """把 JSON 字符串格式化为带缩进的漂亮格式"""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        return f"❌ JSON 解析失败: {e}"

    pretty = json.dumps(obj, ensure_ascii=False, indent=indent, sort_keys=sort_keys)
    return pretty


@mcp.tool()
async def minify_json(raw: str, sort_keys: bool = True) -> str:
    """把 JSON 字符串压缩成单行，去掉所有空白字符"""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        return f"❌ JSON 解析失败: {e}"

    mini = json.dumps(
        obj, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys
    )
    return mini


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
