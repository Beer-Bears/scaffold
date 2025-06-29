__all__ = ["get_settings", "MainSettings", "EnvBasedSettings"]
from functools import lru_cache

from pydantic_settings import BaseSettings

from src.core.vector.config import VectorSettings
from src.database.config import DatabaseSettings


class EnvBasedSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class MainSettings(EnvBasedSettings, DatabaseSettings, VectorSettings):
    project_name: str = "Scaffold"
    project_description: str = "Specialized RAG system for large codebases"
    version: str = "0.1.0"
    environment: str = "development"


@lru_cache()
def get_settings() -> MainSettings:
    return MainSettings()
