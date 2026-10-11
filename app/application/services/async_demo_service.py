import asyncio
import time
from collections.abc import AsyncIterator
from typing import Any

async def fetch_user_profile() ->dict[str, Any]:
    await asyncio.sleep(1)
    return {
        "user_id": "user_001",
        "name": "Demo User",
    }
async def search_knowledge_base() -> list[str]:
    """模拟异步检索知识库。"""
    await asyncio.sleep(1.5)

    return [
        "知识片段 A",
        "知识片段 B",
    ]

async def run_parallel_tasks() -> dict[str, Any]:
    """并发执行彼此独立的异步 I/O 操作。"""
    started_at = time.perf_counter()

    profile, documents = await asyncio.gather(
        fetch_user_profile(),
        search_knowledge_base(),
    )

    elapsed_ms = (time.perf_counter() - started_at) * 1000

    return {
        "profile": profile,
        "documents": documents,
        "elapsed_ms": round(elapsed_ms, 2),
    }

async def run_with_timeout(
    timeout_seconds: float = 1.0,
) -> str:
    """在指定时间内完成操作，否则触发超时。"""
    async with asyncio.timeout(timeout_seconds):
        await asyncio.sleep(5)

    return "completed"


async def generate_answer_stream() -> AsyncIterator[str]:
    """模拟模型逐段生成答案。"""
    chunks = [
        "你好，",
        "欢迎学习 ",
        "FastAPI 流式响应。",
    ]

    for chunk in chunks:
        await asyncio.sleep(0.3)
        yield chunk
