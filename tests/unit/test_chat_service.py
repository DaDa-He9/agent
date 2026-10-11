import asyncio

from app.application.services.chat_service import ChatService
from app.domain.models.chat import ChatResult


class FakeChatRepository:
    async def save(
        self,
        *,
        user_id: str,
        message: str,
        status: str,
    ) -> ChatResult:
        return ChatResult(
            user_id=user_id,
            message=message,
            status=status,
        )


def test_chat_service_returns_saved_result() -> None:
    async def run_test() -> None:
        service = ChatService(FakeChatRepository())

        result = await service.execute(
            user_id="user_001",
            message="你好",
        )

        assert result == ChatResult(
            user_id="user_001",
            message="你好",
            status="received",
        )

    asyncio.run(run_test())