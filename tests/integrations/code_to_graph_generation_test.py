import pathlib

import pytest
from neomodel import db, clear_neo4j_database, config
from testcontainers.neo4j import Neo4jContainer

from src.generator.generator import save_graph_to_db
from src.parsers.python.core import Parser

PROJECTS = ["syntatic-1", "realworld-1"]


@pytest.fixture(scope="module", autouse=True)
def setup_test_db(neo4j_container: Neo4jContainer):
    host, port = neo4j_container.get_container_host_ip(), neo4j_container.get_exposed_port(7687)
    config.DATABASE_URL = f"bolt://neo4j:password@{host}:{port}"
    yield


@pytest.fixture(scope="session")
def neo4j_container():
    with Neo4jContainer(username="neo4j", password="password") as container:
        yield container


@pytest.fixture(scope="function", autouse=True)
def clear_db_for_each_test():
    clear_neo4j_database(db)


@pytest.mark.parametrize("project", PROJECTS)
def test_project_parsing_and_saving(project: str, setup_test_db):
    """
    Tests that a project is parsed correctly and saved to the database.
    """
    parser = Parser(pathlib.Path(f"codebase/{project}"))
    parser.parse()
    assert parser.nodes

    save_graph_to_db(parser.nodes)

    file_count, _ = db.cypher_query("MATCH (n:FileNode) RETURN count(n)")
    class_count, _ = db.cypher_query("MATCH (n:ClassNode) RETURN count(n)")
    function_count, _ = db.cypher_query("MATCH (n:FunctionNode) RETURN count(n)")

    file_count = file_count[0][0]
    class_count = class_count[0][0]
    function_count = function_count[0][0]


    if project == "syntatic-1":
        assert file_count == 7
        assert class_count == 4
        assert function_count == 44
    elif project == "realworld-1":
        assert file_count == 11
        assert class_count == 9
        assert function_count == 95
