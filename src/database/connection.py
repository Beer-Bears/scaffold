__all__ = ["init_chromadb", "init_neo4j"]
import chromadb
from chromadb.config import Settings as ChromaSettings
from llama_index.vector_stores.chroma import ChromaVectorStore
from neomodel import config  # type: ignore[import-untyped]

from src.core.config import get_settings

settings = get_settings()

# --- ChromaDB ---
# https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/


def init_chromadb() -> ChromaVectorStore:
    chroma_settings = ChromaSettings(
        chroma_server_host=settings.database.chromadb_host,
        chroma_server_http_port=settings.database.chromadb_port,
    )
    client = chromadb.HttpClient(
        host=settings.database.chromadb_host,
        port=settings.database.chromadb_port,
        settings=chroma_settings,
    )
    client.heartbeat()

    chroma_collection = client.get_or_create_collection(
        settings.database.chromadb_collection
    )
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    return vector_store


# --- Neo4j ---
def init_neo4j():
    """
    call in main
    """
    config.DATABASE_URL = settings.database.neo4j_uri
