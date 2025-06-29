__all__ = ["settings", "Settings"]
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    neo4j_uri: Annotated[str, Field(env="NEO4J_URI")]
    neo4j_user: Annotated[str, Field(env="NEO4J_USER")]
    neo4j_password: Annotated[str, Field(env="NEO4J_PASSWORD")]

    chromadb_collection: Annotated[str, Field(env="CHROMA_COLLECTION_NAME")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()  # type: ignore[call-arg]
