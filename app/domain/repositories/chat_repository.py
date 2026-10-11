from typing import Protocol

from app.domain.models.chat import ChatResult


class ChatRepository(Protocol):
    async def save(
        self,
        *,
        user_id: str,
        message: str,
        status: str,
    ) -> ChatResult:
        ...