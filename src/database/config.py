from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(env="DATABASE_URL")
    neo4j_uri: str = Field(env="NEO4J_URI")
    neo4j_user: str = Field(env="NEO4J_USER")
    neo4j_password: str = Field(env="NEO4J_PASSWORD")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
