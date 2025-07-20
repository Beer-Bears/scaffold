import pathlib

from src.core.config import get_settings
from src.core.vector.chunker import chunk_and_load_to_vectorstore
from src.database.connection import init_chromadb, init_neo4j
from src.database.health import check_neo4j
from src.generator.generator import save_graph_to_db
from src.parsers.python.core import Parser

settings = get_settings()
PROJECT_PATH = "./codebase/"


def run_indexing(force_reinit: bool = False):
    """
    Runs the indexing process.                                                                                                                                  │

    :param force_reinit: If True, clears the databases before indexing.                                                                                         │
    """
    init_neo4j()
    if not force_reinit:
        check_neo4j()

    vectorstore = init_chromadb()

    parser = Parser(pathlib.Path(PROJECT_PATH))
    parser.parse()

    save_graph_to_db(parser.nodes)

    chunk_and_load_to_vectorstore(
        vector_store=vectorstore,
        root_dir=PROJECT_PATH,
    )
