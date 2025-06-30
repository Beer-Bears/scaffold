__all__ = ["get_splitter"]
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.core.config import get_settings

settings = get_settings().vector


def get_splitter(
    file_identifier: str,
    *,
    chunk_size: int = settings.chunk_size,
    chunk_overlap: int = settings.chunk_overlap
):
    """
    Returns appropriate text splitter for the file type

    Args:
        file_extension: File extension including dot (e.g., '.py', 'file.py', '/path/to/file.js')
        chunk_size: Desired chunk size in characters
        chunk_overlap: Chunk overlap in characters

    Returns:
        Configured text splitter instance
    """
    if "." in file_identifier:
        if file_identifier.startswith("."):  # (e.g., '.py')
            extension = file_identifier.lower()
        else:  # (e.g., 'file.py', '/path/to/file.js')
            extension = os.path.splitext(file_identifier)[1].lower()
    else:
        extension = None

    language = settings.language_dict.get(extension, None)

    # Language-specific splitters
    if language:
        return RecursiveCharacterTextSplitter.from_language(
            language=language, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    # Fallback to generic recursive splitter
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
