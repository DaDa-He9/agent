"""
@Time    :2026/10/11 11:08
@Author  :Dave
@File    :dependencies_demo.py
"""
import logging
from typing import Annotated

from fastapi import Depends

logger = logging.getLogger(__name__)


def get_token() -> str:
    logger.info("1. get_token 执行")
    return "demo-token"


def get_current_user(
    token: Annotated[str, Depends(get_token)],
) -> dict[str, str]:
    logger.info("2. get_current_user 执行")

    return {
        "user_id": "user_001",
        "token": token,
    }