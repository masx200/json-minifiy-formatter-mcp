#!/usr/bin/env python3
"""
MCP server: JSON 格式化 / 压缩
协议：streamable-http
工具：
  - format_json(raw:str, indent:int=2, sort_keys:bool=True) -> str
  - minify_json(raw:str, sort_keys:bool=True) -> str
"""
import json
import os

import anyio
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# 获取环境变量中的HTTP API Token
HTTP_API_TOKEN = os.getenv("HTTP_API_TOKEN")

mcp = FastMCP("json-tools", port=6600, host="0.0.0.0")


@mcp.tool()
async def format_json(raw: str, indent: int = 2, sort_keys: bool = True) -> str:
    """把 JSON 字符串格式化为带缩进的漂亮格式"""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")
        # return f"❌ JSON 解析失败: {e}"

    pretty = json.dumps(obj, ensure_ascii=False, indent=indent, sort_keys=sort_keys)
    return pretty


from starlette.types import ASGIApp


@mcp.tool()
async def minify_json(raw: str, sort_keys: bool = True) -> str:
    """把 JSON 字符串压缩成单行，去掉所有空白字符"""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")
        # return f"❌ JSON 解析失败: {e}"

    mini = json.dumps(
        obj, ensure_ascii=False, separators=(",", ":"), sort_keys=sort_keys
    )
    return mini

class FixedBearerTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, token: str):
        super().__init__(app)
        self.token = token

    async def dispatch(self, request, call_next):
        auth_header = request.headers.get("authorization")
        expected = f"Bearer {self.token}"
        if auth_header != expected:
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)
        return await call_next(request)
async def run_streamable_http_async(mcp:FastMCP, HTTP_API_TOKEN:str):

    starlette_app = mcp.streamable_http_app()
     # ✅ 添加固定 Token 验证中间件
    starlette_app.add_middleware(
        FixedBearerTokenMiddleware,
        token=HTTP_API_TOKEN
    )

    config = uvicorn.Config(
        starlette_app,
        host=mcp.settings.host,
        port=mcp.settings.port,
        log_level=mcp.settings.log_level.lower(),
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    if HTTP_API_TOKEN:
        print(f"使用环境变量 HTTP API Token: {HTTP_API_TOKEN}")
        anyio.run(run_streamable_http_async, mcp, HTTP_API_TOKEN)

    else:
        print("未设置环境变量 HTTP API Token")
        mcp.run(transport="streamable-http")
