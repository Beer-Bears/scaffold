import ast
import logging
import sys
from typing import Dict, Optional, Tuple

from src.generator.graph_types import NodeType, RelationshipType
from src.generator.models import Node, Relationship

logging.StreamHandler(sys.stdout)
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ImportNodeVisitor(ast.NodeVisitor):
    def __init__(self, path, files: Dict[int, Node]):
        self.path = path
        self.nodes = files
        self.scope_stack: list[str] = []

    type SupportedNode = ast.ClassDef | ast.FunctionDef | ast.Call | ast.AsyncFunctionDef

    # 3 cases:
    #  1. relative import with some level (>0)
    #  - absolute import (level=0):
    #    2. some external lib
    #    3. project package

    def visit_Import(self, node: ast.Import):
        """
        Import files
        ast.Import:
            - names: [import src.database, fastapi]
        """
        # case 1: not possible - https://docs.python.org/3/reference/import.html#:~:text=but%20relative%20imports
        # case 2: ignore
        # case 3:
        imported_modules_str = [n.name for n in node.names]
        # current file - always should exist
        exist, importing_file_id, _ = self.match_file_by_path(self.path)
        assert exist is True and importing_file_id is not None

        for imported_module_str in imported_modules_str:


            imported_file_path, imported_module_path = self.module_to_py_path(
                imported_module_str
            )

            # find either single file or module
            matched, imported_file_id, imported_file = self.match_file_by_path(
                imported_file_path
            )
            if not matched:
                matched, imported_file_id, imported_file = self.match_file_by_path(
                    imported_module_path
                )

            if matched:
                self.add_import_relation(
                    importing=importing_file_id, imported=imported_file_id
                )

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        ast.ImportFrom:
            - module: [src.main]
            - level: 2 [from ..module import some]
            - names: [from src import some, some2]
              - some, some2
        """
        module = node.module
        level = node.level
        imported_nodes_str = [n.name for n in node.names]

        # case 1:
        #  get relative file from current
        # case 3:
        #  recursively try to match import to some path
        # case 2:
        #  if didn't match - ignore

        # current file - always should exist
        exist, importing_file_id, _ = self.match_file_by_path(self.path)
        assert exist is True and importing_file_id is not None

        if level > 0:  # case 1 todo
            return

        file_path, module_path = self.module_to_py_path(module)
        matched, file_id, file = self.match_file_by_path(file_path)
        if not matched:
            matched, file_id, file = self.match_file_by_path(module_path)

        if not matched:  # case 2
            return
        # so its matched

        # case 3
        for imported_node_str in imported_nodes_str:

            imported_node_id = self.find_top_lvl_node_in_file(file, imported_node_str)

            if imported_node_id is not None:
                self.add_import_relation(
                    importing=importing_file_id, imported=imported_node_id
                )


    def match_file_by_path(
        self, path: str
    ) -> Tuple[bool, Optional[int], Optional[Node]]:
        for _id, node in self.nodes.items():
            if node._type is NodeType.FILE and node.meta.path == path:
                return True, _id, node

        for _id, node in self.nodes.items():
            if node._type is NodeType.FILE and path in node.meta.path:
                return True, _id, node

        return False, None, None

    def add_import_relation(self, importing: int, imported: int):
        assert type(importing) is int, type(importing)
        assert type(imported) is int, type(imported)
        self.nodes[importing].relationships.append(
            Relationship(
                relation_type=RelationshipType.IMPORT, parent=importing, node=imported
            )
        )

    def find_top_lvl_node_in_file(
        self, file: Node, imported_node_str: str
    ) -> Optional[int]:
        for node_id in [r.node for r in file.relationships]:
            if self.nodes[node_id].meta.name == imported_node_str:
                return node_id


    def module_to_py_path(self, module: str) -> Tuple[str, str]:
        """
        src.database.config -> (src/database/config.py, src/database/config/__init__.py)
        my_project -> (my_project.py, my_project/__init__.py)
        """
        path = module.replace(".", "/")
        return path + ".py", path + "/__init__.py"
