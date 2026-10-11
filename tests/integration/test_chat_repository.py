import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.domain.models.chat import ChatResult
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.chat_message import ChatMessageORM
from app.infrastructure.database.repositories.sqlalchemy_chat_repository import (
    SQLAlchemyChatRepository,
)


def test_repository_persists_chat_message(tmp_path) -> None:
    async def run_test() -> None:
        database_file = tmp_path / "test_chat.db"
        database_url = f"sqlite+aiosqlite:///{database_file}"

        test_engine = create_async_engine(database_url)
        test_session_factory = async_sessionmaker(
            bind=test_engine,
            expire_on_commit=False,
        )

        try:
            async with test_engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)

            async with test_session_factory() as session:
                repository = SQLAlchemyChatRepository(session)

                result = await repository.save(
                    user_id="user_test",
                    message="请介绍一下 RAG",
                    status="received",
                )

                assert result == ChatResult(
                    user_id="user_test",
                    message="请介绍一下 RAG",
                    status="received",
                )

            async with test_session_factory() as session:
                statement = select(ChatMessageORM).where(
                    ChatMessageORM.user_id == "user_test"
                )
                query_result = await session.execute(statement)
                record = query_result.scalar_one()

                assert record.message == "请介绍一下 RAG"
                assert record.status == "received"
                assert record.id is not None
                assert record.created_at is not None

        finally:
            await test_engine.dispose()

    asyncio.run(run_test())