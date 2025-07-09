import os

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.core.config import get_settings

# SimpleDirectoryReader
# https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader/#simpledirectoryreader
settings = get_settings().vector


def get_meta(file_path):
    return {"file_path": file_path}


def chunk_and_load_to_vectorstore(
    vector_store: ChromaVectorStore, root_dir: str
) -> VectorStoreIndex:
    """
    Processes all files in a directory, splits them into chunks, and loads into ChromaDB
    """

    all_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            all_files.append(full_path)

    # TODO: Implement .ignore functionality

    reader = SimpleDirectoryReader(input_files=all_files, file_metadata=get_meta)

    documents = reader.load_data(show_progress=True, num_workers=4)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=settings.embed_model
    )

    return index
