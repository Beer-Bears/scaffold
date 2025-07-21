import logging
import time
from pathlib import Path

from src.core.config import get_settings
from src.core.vector.chunker import chunk_and_load_to_vectorstore
from src.database.connection import init_chromadb, init_neo4j
from src.database.health import check_neo4j
from src.generator.generator import save_graph_to_db
from src.parsers.python.core import Parser

settings = get_settings()
logger = logging.getLogger(__name__)


def run_full_indexing(path: str | Path, force_reinit: bool = False):
    """
    Runs the indexing process.

    :param path: Path of the codebase to be indexed.
    :param force_reinit: If True, clears the databases before indexing.
    """
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("neo4j").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger.info("[Indexer] Starting indexing process...")
    logger.info(f"[Indexer] Project path set to: {path}")
    start_time = time.time()

    init_neo4j(force_reinit=force_reinit)

    if not force_reinit:
        check_neo4j()

    vectorstore = init_chromadb(force_reinit=force_reinit)

    parser = Parser(path)
    parser.parse()

    save_graph_to_db(parser.nodes)

    chunk_and_load_to_vectorstore(
        vector_store=vectorstore,
        root_dir=str(path),
    )
    duration = time.time() - start_time
    logger.info(f"[Indexer] Indexing process finished in {duration:.2f} seconds.")


def run_indexing(file_path: str | Path):
    """
    Runs the indexing process for a single file.

    :param file_path: Path of the file to be indexed.
    """
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("neo4j").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger.info(f"[Indexer] Starting indexing process for file: {file_path}")
    start_time = time.time()

    init_neo4j()
    check_neo4j()

    parser = Parser(file_path)
    parser.parse()

    save_graph_to_db(parser.nodes)

    duration = time.time() - start_time
    logger.info(
        f"[Indexer] Indexing process for file finished in {duration:.2f} seconds."
    )
