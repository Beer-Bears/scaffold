__all__ = ["get_splitter"]
import os
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)

# Language extension mapping
EXTENSION_TO_LANGUAGE = {
    '.py': Language.PYTHON,
    '.js': Language.JS,
    '.jsx': Language.JS,
    '.ts': Language.JS,
    '.tsx': Language.JS,
    '.java': Language.JAVA,
    '.kt': Language.KOTLIN,
    '.cpp': Language.CPP,
    '.go': Language.GO,
    '.rb': Language.RUBY,
    '.rs': Language.RUST,
    '.php': Language.PHP,
    '.swift': Language.SWIFT,
    '.cs': Language.CSHARP,
    '.pl': Language.PERL,
    '.lua': Language.LUA,
    '.html': Language.HTML,
    '.htm': Language.HTML,
    '.md': Language.MARKDOWN,
    '.markdown': Language.MARKDOWN,
    '.tex': Language.LATEX,
}

# Customizable splitter parameters
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50

def get_splitter(file_identifier: str, 
                 chunk_size: int = DEFAULT_CHUNK_SIZE, 
                 chunk_overlap: int = DEFAULT_CHUNK_OVERLAP):
    """
    Returns appropriate text splitter for the file type
    
    Args:
        file_extension: File extension including dot (e.g., '.py', 'file.py', '/path/to/file.js')
        chunk_size: Desired chunk size in characters
        chunk_overlap: Chunk overlap in characters
    
    Returns:
        Configured text splitter instance
    """
    if '.' in file_identifier: 
        if file_identifier.startswith('.'): # (e.g., '.py')
            extension = file_identifier.lower()
        else: # (e.g., 'file.py', '/path/to/file.js')
            extension = os.path.splitext(file_identifier)[1].lower()
    else:
        extension = None

    language = EXTENSION_TO_LANGUAGE.get(extension, None)
    
    # Language-specific splitters
    if language:
        return RecursiveCharacterTextSplitter.from_language(
            language=language,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    # Fallback to generic recursive splitter
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )