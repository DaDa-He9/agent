import logging
from fastapi import APIRouter,Request

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check(request:Request) -> dict[str, str]:
    logger.info(
        "Health check requested: method=%s path=%s",
        request.method,
        request.url.path,
    )

    return {"status": "ok"}
