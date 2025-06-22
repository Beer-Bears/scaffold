import asyncio
import pathlib
from src.database.connection import init_neo4j
from src.database.health import check as test_db, check_neo4j
from src.generator.generator import save_graph_to_db
from src.parsers.python.core import Parser

if __name__ == '__main__':
    # asyncio.run(test_db())

    init_neo4j()
    check_neo4j()
    parser = Parser(pathlib.Path("./codebase"))
    parser.parse()
    
    save_graph_to_db(parser.nodes)

