import pathlib

from src.core.config import get_settings
from src.core.vector.chunker import chunk_and_load_to_vectorstore
from src.database.connection import init_chromadb, init_neo4j
from src.database.health import check_neo4j
from src.generator.generator import save_graph_to_db
from src.mcp.server import mcp
from src.parsers.python.core import Parser

settings = get_settings()

PROJECT_PATH = "./codebase/"

if __name__ == "__main__":

    init_neo4j()
    check_neo4j()

    parser = Parser(pathlib.Path(PROJECT_PATH))
    parser.parse()

    # TODO: Remove double indexing
    save_graph_to_db(parser.nodes)
    vectorstore = init_chromadb()

    chunk_and_load_to_vectorstore(
        vector_store=vectorstore,
        root_dir=PROJECT_PATH,
    )

    # MCP Inteface
    mcp.run(**settings.mcp_server.model_dump())
