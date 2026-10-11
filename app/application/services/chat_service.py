"""
@Time    :2026/10/11 14:04
@Author  :Dave
@File    :chat_service.py
"""
from app.domain.models.chat import ChatResult
from app.domain.repositories.chat_repository import ChatRepository


class ChatService:
    def __init__(self, repository: ChatRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        *,
        user_id: str,
        message: str,
    ) -> ChatResult:
        return await self._repository.save(
            user_id=user_id,
            message=message,
            status="received",
        )