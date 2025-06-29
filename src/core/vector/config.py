from typing import Annotated

from langchain_text_splitters import Language
from pydantic_settings import BaseSettings

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 100

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

    chunk_size = Annotated[int, DEFAULT_CHUNK_SIZE]
    chunk_overlap = Annotated[int, DEFAULT_CHUNK_OVERLAP]

    language_dict = Annotated[dict[str, Language], EXTENSION_TO_LANGUAGE]
