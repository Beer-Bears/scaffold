import logging

import chromadb
from chromadb.config import Settings as ChromaSettings

from src.core.config import get_settings

logger = logging.getLogger(__name__)


def delete_from_vectorstore_by_path(file_path: str):
    """
    Deletes documents from the ChromaDB vector store based on the file_path metadata.
    """
    settings = get_settings()
    try:
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
        collection = client.get_collection(settings.database.chromadb_collection)

        # 3. Delete documents by metadata
        collection.delete(where={"file_path": file_path})
        logger.info(f"Deleted vectors from ChromaDB for file: {file_path}")

    except Exception as e:
        # This can happen if the collection doesn't exist, which is fine.
        logger.warning(f"Could not delete vectors for file {file_path}: {e}")
