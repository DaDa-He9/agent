from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.chat import ChatResult
from app.domain.repositories.chat_repository import ChatRepository
from app.infrastructure.database.models.chat_message import ChatMessageORM


class SQLAlchemyChatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(
        self,
        *,
        user_id: str,
        message: str,
        status: str,
    ) -> ChatResult:
        record = ChatMessageORM(
            user_id=user_id,
            message=message,
            status=status,
        )
        self._session.add(record)

        try:
            await self._session.commit()
            await self._session.refresh(record)
        except Exception:
            await self._session.rollback()
            raise

        return ChatResult(
            user_id=record.user_id,
            message=record.message,
            status=record.status,
        )