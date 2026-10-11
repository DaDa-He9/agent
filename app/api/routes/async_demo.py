import asyncio
import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.application.services.async_demo_service import (
    generate_answer_stream,
    run_parallel_tasks,
    run_with_timeout,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/parallel-demo")
async def parallel_demo() -> dict:
    return await run_parallel_tasks()


@router.get("/timeout-demo")
async def timeout_demo() -> dict[str, str]:
    try:
        result = await run_with_timeout(timeout_seconds=1.0)
        return {"status": result}
    except TimeoutError as exc:
        logger.warning("Demo operation timed out")
        raise HTTPException(
            status_code=504,
            detail="上游操作超时",
        ) from exc


@router.get("/stream-demo")
async def stream_demo() -> StreamingResponse:
    return StreamingResponse(
        generate_answer_stream(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )