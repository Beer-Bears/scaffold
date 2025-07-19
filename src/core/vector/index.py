__all__ = ["get_existing_chroma_index"]
import chromadb
from chromadb.config import Settings as ChromaSettings
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.core.config import get_settings

settings = get_settings()


def get_existing_chroma_index() -> VectorStoreIndex:
    # 1. Initialize Chroma client
    chroma_settings = ChromaSettings(
        chroma_server_host=settings.database.chromadb_host,
        chroma_server_http_port=settings.database.chromadb_port,
    )
    client = chromadb.HttpClient(
        host=settings.database.chromadb_host,
        port=settings.database.chromadb_port,
        settings=chroma_settings,
    )

    # 2. Get existing collection
    chroma_collection = client.get_collection(settings.database.chromadb_collection)

    # 3. Wrap in LlamaIndex vector store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # 4. Create index from existing store
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store, embed_model=settings.vector.embed_model
    )

    return index
