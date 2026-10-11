"""
@Time    :2026/10/11 10:37
@Author  :Dave
@File    :chat.py
"""
from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    message: str = Field(
        min_length=1,
        max_length=2000,
        description="用户发送的消息",
        examples=["请介绍一下 RAG"],
    )


class ChatResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str
    message: str
    status: str = "received"
