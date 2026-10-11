"""
@Time    :2026/10/11 10:54
@Author  :Dave
@File    :dependencies.py
"""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.chat_repository import ChatRepository
from app.infrastructure.database.repositories.sqlalchemy_chat_repository import (
    SQLAlchemyChatRepository,
)
from app.infrastructure.database.session import get_db_session


def get_current_user_id() -> str:
    # 课程阶段使用固定用户 ID；后续会接入真实认证。
    return "user_001"


CurrentUserId = Annotated[str, Depends(get_current_user_id)]


def get_chat_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ChatRepository:
    return SQLAlchemyChatRepository(session)