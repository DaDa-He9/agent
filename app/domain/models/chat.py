from dataclasses import dataclass


@dataclass(frozen=True)
class ChatResult:
    user_id: str
    message: str
    status: str