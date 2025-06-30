__all__ = ["get_settings", "AppSettings"]
from functools import lru_cache
from typing import Annotated, Literal

from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import Language
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

EXTENSION_TO_LANGUAGE = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".jsx": Language.JS,
    ".ts": Language.JS,
    ".tsx": Language.JS,
    ".java": Language.JAVA,
    ".kt": Language.KOTLIN,
    ".cpp": Language.CPP,
    ".go": Language.GO,
    ".rb": Language.RUBY,
    ".rs": Language.RUST,
    ".php": Language.PHP,
    ".swift": Language.SWIFT,
    ".cs": Language.CSHARP,
    ".pl": Language.PERL,
    ".lua": Language.LUA,
    ".html": Language.HTML,
    ".htm": Language.HTML,
    ".md": Language.MARKDOWN,
    ".markdown": Language.MARKDOWN,
    ".tex": Language.LATEX,
}


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

    # Splitter
    language_dict: dict[str, Language] = EXTENSION_TO_LANGUAGE

    # Common
    embedings_function: Embeddings = HuggingFaceEmbeddings()


class DatabaseSettings(BaseSettings):
    neo4j_uri: Annotated[str, Field(env="NEO4J_URI")]
    neo4j_user: Annotated[str, Field(env="NEO4J_USER")]
    neo4j_password: Annotated[str, Field(env="NEO4J_PASSWORD")]

    chromadb_collection: Annotated[str, Field(env="CHROMA_COLLECTION_NAME")] = (
        "default_collection"
    )


class MCPServerSettings(BaseSettings):
    transport: Literal["stdio", "http", "sse", "streamable-http"] = "http"
    host: str = "0.0.0.0"
    port: int = 8000


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
