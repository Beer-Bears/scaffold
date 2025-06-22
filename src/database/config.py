from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: Annotated[str, Field(env="DATABASE_URL")]
    neo4j_uri: Annotated[str, Field(env="NEO4J_URI")]
    neo4j_user: Annotated[str, Field(env="NEO4J_USER")]
    neo4j_password: Annotated[str, Field(env="NEO4J_PASSWORD")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()  # type: ignore[call-arg]
