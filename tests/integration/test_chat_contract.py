"""
@Time    :2026/10/11 14:09
@Author  :Dave
@File    :test_chat_contract.py
"""
import pytest
from fastapi.testclient import TestClient

from app.api.routes.chat import get_chat_service
from app.application.services.chat_service import ChatService
from app.domain.models.chat import ChatResult
from app.main import app


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


@pytest.fixture
def client():
    app.dependency_overrides[get_chat_service] = (
        lambda: ChatService(FakeChatRepository())
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_chat_service, None)


def test_chat_response_matches_contract(client: TestClient) -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": "你好"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": "user_001",
        "message": "你好",
        "status": "received",
    }


def test_chat_rejects_extra_fields(client: TestClient) -> None:
    response = client.post(
        "/api/v1/chat",
        json={"message": "你好", "debug": True},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    assert response.headers.get("X-Request-ID")