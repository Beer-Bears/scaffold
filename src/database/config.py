__all__ = ["DatabaseSettings"]
from typing import Annotated

from pydantic import Field

from src.core.config import EnvBasedSettings


class DatabaseSettings(EnvBasedSettings):

    neo4j_uri: Annotated[str, Field(env="NEO4J_URI")]
    neo4j_user: Annotated[str, Field(env="NEO4J_USER")]
    neo4j_password: Annotated[str, Field(env="NEO4J_PASSWORD")]

    chromadb_collection: Annotated[str, Field(env="CHROMA_COLLECTION_NAME")]
