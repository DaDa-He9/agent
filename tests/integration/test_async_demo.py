from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_parallel_tasks_complete() -> None:
    response = client.get("/api/v1/parallel-demo")

    assert response.status_code == 200

    body = response.json()

    assert body["profile"]["user_id"] == "user_001"
    assert body["documents"] == [
        "知识片段 A",
        "知识片段 B",
    ]

    # 两个操作各等待约 1.5 秒，并发总耗时通常明显小于 3 秒。
    assert body["elapsed_ms"] < 2800


def test_timeout_returns_504() -> None:
    response = client.get("/api/v1/timeout-demo")

    assert response.status_code == 504
    assert response.headers.get("X-Request-ID")

    body = response.json()

    assert body["error"]["code"] == "HTTP_ERROR"
    assert body["error"]["message"] == "上游操作超时"


def test_stream_response_returns_all_chunks() -> None:
    response = client.get("/api/v1/stream-demo")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert response.headers.get("X-Request-ID")

    assert response.text == (
        "你好，"
        "欢迎学习 "
        "FastAPI 流式响应。"
    )