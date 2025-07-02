__all__ = ["get_retriever"]
from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

from src.core.config import get_settings

settings = get_settings().vector


@lru_cache
def get_retriever(
    vector_store: Chroma,
    k: int = settings.k,
    search_type: str = settings.similarity_type,
    search_kwargs: dict = {},
) -> VectorStoreRetriever:
    search_kwargs.update({"k": k})
    retriever = vector_store.as_retriever(
        search_type=search_type, search_kwargs=search_kwargs
    )
    return retriever
