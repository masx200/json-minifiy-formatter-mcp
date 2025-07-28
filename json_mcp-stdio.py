#!/usr/bin/env python3
"""
MCP server: JSON 格式化 / 压缩
协议：stdio
工具：
  - format_json(raw:str, indent:int=2, sort_keys:bool=True) -> str
  - minify_json(raw:str, sort_keys:bool=True) -> str
"""
import json

import asyncio

from mcp import types
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server

server = Server("json-tools")


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    # types.CallToolResult:
    """处理 tool 调用"""
    if name == "format_json":
        try:
            obj = json.loads(arguments["raw"])
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败: {e}")
            # return types.CallToolResult(content=[types.TextContent(type="text", text=f"❌ JSON 解析失败: {e}")], isError=True)

        indent = arguments.get("indent", 2)
        sort_keys = arguments.get("sort_keys", True)
        pretty = json.dumps(obj, ensure_ascii=False, indent=indent, sort_keys=sort_keys)
        return [types.TextContent(type="text", text=pretty)]
        # return types.CallToolResult(content=[types.TextContent(type="text", text=pretty)])

    elif name == "minify_json":
        try:
            obj = json.loads(arguments["raw"])
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败: {e}")
            # return types.CallToolResult(content=[types.TextContent(type="text", text=f"❌ JSON 解析失败: {e}")], isError=True)

        sort_keys = arguments.get("sort_keys", True)
        mini = json.dumps(
            obj, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys
        )
        return [types.TextContent(type="text", text=mini)]
        # return types.CallToolResult(content=[types.TextContent(type="text", text=mini)])

    else:
        return [types.TextContent(type="text", text=f"未知工具: {name}")]
        # return types.CallToolResult(content=[types.TextContent(type="text", text=f"未知工具: {name}")], isError=True)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """声明两个工具"""
    return [
        types.Tool(
            name="format_json",
            description="把 JSON 字符串格式化为带缩进的漂亮格式",
            inputSchema={
                "type": "object",
                "properties": {
                    "raw": {"type": "string", "description": "原始 JSON 字符串"},
                    "indent": {
                        "type": "integer",
                        "default": 2,
                        "description": "缩进空格数",
                    },
                    "sort_keys": {
                        "type": "boolean",
                        "default": True,
                        "description": "是否对键排序",
                    },
                },
                "required": ["raw"],
            },
        ),
        types.Tool(
            name="minify_json",
            description="把 JSON 字符串压缩成单行，去掉所有空白字符",
            inputSchema={
                "type": "object",
                "properties": {
                    "raw": {"type": "string", "description": "原始 JSON 字符串"},
                    "sort_keys": {
                        "type": "boolean",
                        "default": True,
                        "description": "是否对键排序",
                    },
                },
                "required": ["raw"],
            },
        ),
    ]



async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(
                notification_options=NotificationOptions(
                    resources_changed=False,
                    tools_changed=False,
                )
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
