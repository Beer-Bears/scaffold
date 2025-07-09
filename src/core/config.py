__all__ = ["get_settings", "AppSettings"]
from functools import lru_cache
from typing import Annotated, Literal

from llama_index.core.embeddings.multi_modal_base import MultiModalEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


DEFAULT_CHUNK_SIZE = 500
DEFAULT_K_RETRIVE = 5
DEFAULT_CHUNK_OVERLAP = 50


class VectorSettings(BaseSettings):
    # Retriever
    k: int = DEFAULT_K_RETRIVE
    similarity_type: str = (
        "similarity",
        "similarity_score_threshold",
        "mmr",
    )[0]

    # Chunker
    chunk_size: int = DEFAULT_CHUNK_SIZE
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP

    # Common
    embed_model: MultiModalEmbedding = HuggingFaceEmbedding(
        model_name="BAAI/bge-base-en-v1.5"
    )


class DatabaseSettings(BaseSettings):
    neo4j_uri: Annotated[str, Field(env="NEO4J_URI")]
    neo4j_user: Annotated[str, Field(env="NEO4J_USER")]
    neo4j_password: Annotated[str, Field(env="NEO4J_PASSWORD")]

    chromadb_collection: Annotated[str, Field(env="CHROMA_COLLECTION_NAME")] = (
        "default_collection"
    )

    chromadb_host: Annotated[str, Field(env="CHROMA_SERVER_HOST")] = "chromadb"
    chromadb_port: Annotated[int, Field(env="CHROMA_SERVER_PORT")] = 8000


class MCPServerSettings(BaseSettings):
    transport: Literal["stdio", "http", "sse", "streamable-http"] = "http"
    host: str = "0.0.0.0"
    port: int = 8080


class AppSettings(BaseModel):
    project_name: str = "Scaffold"
    project_description: str = "Specialized RAG system for large codebases"
    version: str = "0.1.0"

    vector: VectorSettings
    database: DatabaseSettings
    mcp_server: MCPServerSettings


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings(
        vector=VectorSettings(),
        database=DatabaseSettings(),
        mcp_server=MCPServerSettings(),
    )
