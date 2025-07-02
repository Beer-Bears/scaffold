import ast
import logging
import sys

from src.parsers.python.models import FileGraph

logging.StreamHandler(sys.stdout)
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ImportNodeVisitor(ast.NodeVisitor):
    def __init__(self, path):
        self.file = FileGraph(path)
        self.scope_stack: list[str] = []

    type SupportedNode = ast.ClassDef | ast.FunctionDef | ast.Call | ast.AsyncFunctionDef

    def visit_Import(self, node: ast.Import):
        print(
            f"Import Node:\n\t{[alias.__dict__['name'] for alias in node.__dict__['names']]}"
        )

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        ast.ImportFrom:
            - module: [src.main]
            - level: 2 [from ..module import some]
            - names: [from src import some, some2]
              - some, some2
        """
        # 3 cases:
        #  1. relative import with some level (>0)
        #  - absolute import (level=0):
        #    2. some external lib
        #    3. project package

        # case 1:
        #  get relative file from current
        # case 3:
        #  recursively try to match import to some path
        # case 2:
        #  if didn't match - ignore
        module = node.module
        level = node.level
        names = [name.name for name in node.names]

        # if level > 0:  # case 1
        #     pass
        # else:
        #     path = module.replace(".", "/")
        #     matched, file_path = try_to_match_path()
        #     if matched:  # case 3
        #         import_from: CodeElement = get_file_node(file_path)
        #         importing: CodeElement = current_file_node
        #         add_relation(importing, import_from, RelationshipType.USE)
        #     else:  # case 2
        #         ...
        print(
            f"Import From Node:\n\tFrom `{'./'*node.__dict__['level']}{node.__dict__['module']}` Import {[alias.__dict__['name'] for alias in node.__dict__['names']]}"
        )
        print("\t", module, level, names)
