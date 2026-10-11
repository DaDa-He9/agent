"""
@Time    :2026/10/11 10:37
@Author  :Dave
@File    :chat.py
"""
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import CurrentUserId, get_chat_repository
from app.application.services.chat_service import ChatService
from app.domain.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


def get_chat_service(
    repository: Annotated[ChatRepository, Depends(get_chat_repository)],
) -> ChatService:
    return ChatService(repository)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: CurrentUserId,
    service: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatResponse:
    result = await service.execute(
        user_id=user_id,
        message=request.message,
    )

    return ChatResponse(
        user_id=result.user_id,
        message=result.message,
        status=result.status,
    )
# @router.get("/dependency_demo")
# async def dependency_demo(user: Annotated[dict[str, str], Depends(get_current_user)],
# ) -> dict[str, str]:
#     return user