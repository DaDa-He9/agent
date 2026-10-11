"""
@Time    :2026/10/11 14:27
@Author  :Dave
@File    :config.py
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用程序配置。"""

    app_name: str = "AI Agent Platform"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str = "sqlite+aiosqlite:///./ai_agent.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """缓存配置，避免重复创建。"""
    return Settings()