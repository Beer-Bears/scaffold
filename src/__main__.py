import pathlib

from src.database.connection import init_neo4j
from src.database.health import check_neo4j
from src.generator.generator import get_node_information, save_graph_to_db
from src.mcp.server import mcp
from src.parsers.python.core import Parser

if __name__ == "__main__":
    # asyncio.run(test_db())

    init_neo4j()
    check_neo4j()
    parser = Parser(pathlib.Path("./codebase"))
    parser.parse()

    save_graph_to_db(parser.nodes)

    while True:
        print("-" * 100, "\n" * 3)
        name = input()
        print(get_node_information(name))
        if name == "exit":
            break

    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
