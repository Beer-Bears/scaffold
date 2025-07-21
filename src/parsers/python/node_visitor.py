import ast
import pathlib
from pprint import pprint

from src.generator.graph_types import NodeType, RelationshipType
from src.parsers.python.models import CodeElement, FileGraph


class NodeVisitor(ast.NodeVisitor):
    def __init__(self, path):
        self.file = FileGraph(path)
        self.scope_stack: list[str] = []

    type SupportedNode = ast.ClassDef | ast.FunctionDef | ast.Call | ast.AsyncFunctionDef

    def _get_type(self, node: SupportedNode) -> NodeType:
        match node:
            case ast.ClassDef():
                return NodeType.CLASS
            case ast.FunctionDef() | ast.Call() | ast.AsyncFunctionDef():
                return NodeType.FUNCTION
            case _:
                raise Exception(f"Unexpected node: {node}")

    def _get_name(self, node: SupportedNode) -> str:
        name = None
        match node:
            case (
                ast.ClassDef(name=n)
                | ast.FunctionDef(name=n)
                | ast.AsyncFunctionDef(name=n)
            ):
                name = n
            case ast.Call(func=f):
                f: ast.expr = f
                name = getattr(f, "id", None) or getattr(f, "attr", None)
        assert name is not None, f"Name of '{node}' is not found!"
        return name

    def _create_code_element(self, node: SupportedNode) -> CodeElement:

        name = self._get_name(node)

        element = CodeElement(
            name=name,
            type=self._get_type(node),
            line_number=node.lineno,
            end_line=getattr(node, "end_lineno", node.lineno),
            docstring="",  # todo
        )
        print(__name__, 86, element)
        return element

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.scope_stack.append(node.name)

        self.file.add_element(
            self.scope_stack,
            self.scope_stack,
            self._create_code_element(node),
            relation_type=RelationshipType.DEFINE,
        )

        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef):
        self.scope_stack.append(node.name)

        self.file.add_element(
            self.scope_stack,
            self.scope_stack,
            self._create_code_element(node),
            relation_type=RelationshipType.DEFINE,
        )

        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.scope_stack.append(node.name)

        self.file.add_element(
            self.scope_stack,
            self.scope_stack,
            self._create_code_element(node),
            relation_type=RelationshipType.DEFINE,
        )

        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_Call(self, node: ast.Call):
        self.scope_stack.append(self._get_name(node))

        keep_scope = True

        if hasattr(node, "func") and hasattr(node.func, "value"):
            keep_scope = False

        # find exist node
        scope, element = self.file.get_node(self.scope_stack, self._get_name(node))

        self.file.add_element(
            scope or self.scope_stack,
            self.scope_stack,
            element or self._create_code_element(node),
            relation_type=RelationshipType.USE,
        )

        if not keep_scope:
            self.scope_stack.pop()
        self.generic_visit(node)
        if keep_scope:
            self.scope_stack.pop()


if __name__ == "__main__":
    path = pathlib.Path("codebase/syntatic-1/test1.py")
    file_paths = [f for f in path.rglob("*.py") if f.is_file()]
    file_paths = [path]
    for file_path in file_paths:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))

        v = NodeVisitor(path.name)
        v.visit(tree)
        pprint(v.file.relations)
