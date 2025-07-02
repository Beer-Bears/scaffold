__all__ = ["init_chromadb", "init_neo4j"]
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from neomodel import config  # type: ignore[import-untyped]

from src.core.config import get_settings

settings = get_settings()

# --- ChromaDB ---
# https://python.langchain.com/docs/integrations/vectorstores/chroma/


def init_chromadb() -> tuple[chromadb.ClientAPI, Chroma]:
    print("establishing connection with chromadb")
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
    print("client established")
    collection = client.get_or_create_collection(settings.database.chromadb_collection)

    vector_store = Chroma(
        client=client,
        collection_name=collection.name,
        embedding_function=settings.vector.embedings_function,
    )

    return (client, vector_store)


# --- Neo4j ---
def init_neo4j():
    """
    call in main
    """
    config.DATABASE_URL = settings.database.neo4j_uri
