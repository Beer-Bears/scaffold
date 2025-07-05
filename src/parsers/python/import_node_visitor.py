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
        # case 1 todo
        # case 2 todo
        # case 3:
        _, importing_file_id, _ = self.match_file_by_path(self.path)
        for imported_str in [alias.name for alias in node.names]:
            print(imported_str)
            if imported_str[0] == ".":  # ignore case 1
                continue
            path = imported_str.replace(".", "/") + ".py"
            matched, file_id, file = self.match_file_by_path(path)
            if matched:  # case 3
                print(__name__, 46, imported_str, matched, file_id, file)
                self.add_import_relation(importing=importing_file_id, imported=file_id)
        print(f"Import Node:\n\t{[alias.__dict__ for alias in node.__dict__['names']]}")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        ast.ImportFrom:
            - module: [src.main]
            - level: 2 [from ..module import some]
            - names: [from src import some, some2]
              - some, some2
        """

        # case 1:
        #  get relative file from current
        # case 3:
        #  recursively try to match import to some path
        # case 2:
        #  if didn't match - ignore
        module = node.module
        level = node.level
        names = [n.name for n in node.names]

        if level > 0:  # case 1 todo
            pass
        else:
            path = module.replace(".", "/")
            matched, file_id, file = self.match_file_by_path(path)
            if matched:  # case 3
                _, importing_file_id, _ = self.match_file_by_path(self.path)
                for imported_node_str in names:
                    imported_node_id = self.find_top_lvl_node_in_file(
                        file, imported_node_str
                    )
                    if imported_node_id is not None:
                        self.add_import_relation(
                            importing=importing_file_id, imported=imported_node_id
                        )
            else:  # case 2 todo
                pass
        print(
            f"Import From Node:\n\tFrom `{'./' * node.__dict__['level']}{node.__dict__['module']}` Import {[alias.__dict__['name'] for alias in node.__dict__['names']]}"
        )
        print("\t", module, level, names)

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
                relation_type=RelationshipType.USE, parent=importing, node=imported
            )
        )

    def find_top_lvl_node_in_file(
        self, file: Node, imported_node_str: str
    ) -> Optional[int]:
        for node_id in [r.node for r in file.relationships]:
            if self.nodes[node_id].meta.name == imported_node_str:
                return node_id

        print(__name__, 114, file.meta.name, imported_node_str, "Not found!")
