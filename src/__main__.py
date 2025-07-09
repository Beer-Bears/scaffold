import pathlib

from src.core.config import get_settings
from src.core.vector.chunker import chunk_and_load_to_vectorstore
from src.database.connection import init_chromadb, init_neo4j
from src.database.health import check_neo4j
from src.generator.generator import get_node_information, save_graph_to_db
from src.mcp.server import mcp
from src.parsers.python.core import Parser

settings = get_settings()

PROJECT_PATH = "./codebase/syntatic-1"

if __name__ == "__main__":
    # asyncio.run(test_db())

    local_test = False

    if not local_test:
        init_neo4j()
        check_neo4j()
    # Graph Generation
    init_neo4j()
    check_neo4j()
    parser = Parser(pathlib.Path(PROJECT_PATH))
    parser.parse()

    if not local_test:
        save_graph_to_db(parser.nodes)
        mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)

    # Vector RAG
    vectorstore = init_chromadb()
    index = chunk_and_load_to_vectorstore(
        vector_store=vectorstore,
        root_dir=PROJECT_PATH,
    )
    retriever = index.as_retriever(
        similarity_top_k=5, choice_batch_size=5, embed_model=settings.vector.embed_model
    )
    responce = retriever.retrieve(
        "Where decorator_odd is used in project?",
    )
    print(*responce, sep="\n")

    while True:
        print("-" * 100, "\n" * 3)
        name = input()
        print(get_node_information(name))
        if name == "exit":
            break

    # MCP Inteface
    mcp.run(**settings.mcp_server.model_dump())
