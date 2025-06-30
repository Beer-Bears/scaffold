import pathlib

from src.core.config import get_settings
from src.core.vector.chunker import chunk_and_load_to_vectorstore
from src.core.vector.retriever import get_retriever
from src.database.connection import init_chromadb, init_neo4j
from src.database.health import check_neo4j
from src.generator.generator import save_graph_to_db
from src.mcp.server import mcp
from src.parsers.python.core import Parser

settings = get_settings()
if __name__ == "__main__":
    # asyncio.run(test_db())

    # Graph Generation

    init_neo4j()
    check_neo4j()
    parser = Parser(pathlib.Path("./codebase"))
    parser.parse()

    save_graph_to_db(parser.nodes)

    # Vector RAG
    client, vectorstore = init_chromadb()
    chunk_and_load_to_vectorstore(
        vector_store=vectorstore,
        root_dir="./codebase/syntatic-1",
    )
    retriever = get_retriever(vectorstore)

    results = retriever.invoke(
        "Where decorator_odd is used in project?",
    )

    # MCP Inteface
    mcp.run(**settings.mcp_server.model_dump())
