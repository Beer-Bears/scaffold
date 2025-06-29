__all__ = ["init_chromadb", "init_neo4j"]
import chromadb
from neomodel import config  # type: ignore[import-untyped]
from langchain_chroma import Chroma

from langchain_huggingface import HuggingFaceEmbeddings
from src.database.config import settings

# --- ChromaDB ---

def init_chromadb() -> tuple[chromadb.ClientAPI, Chroma]:
    client = chromadb.Client() # TODO: change to persistent client 
    collection = client.get_or_create_collection(settings.chromadb_collection)

    vector_store = Chroma(
        client=client,
        collection_name=collection.name,
        embedding_function=HuggingFaceEmbeddings(),
    )

    return (client, vector_store)

# --- Neo4j ---
def init_neo4j():
    """
    call in main
    """
    config.DATABASE_URL = settings.neo4j_uri
