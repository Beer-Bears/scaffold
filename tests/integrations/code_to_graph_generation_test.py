import pathlib

import pytest
from neomodel import db

from src.generator.generator import save_graph_to_db
from src.parsers.python.core import Parser
from tests.integrations.conftest import setup_test_db

PROJECTS = ["syntatic-1", "realworld-1"]


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
