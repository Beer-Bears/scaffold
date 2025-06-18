import pathlib
import ast
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field

from src.generator.models import Node, Relationship, MetaInfo
from src.generator.types import NodeType, RelationshipType


@dataclass
class CodeElement:
    """
    Represents a single code element (class, function, method) found in a file.
    Includes details necessary for graph construction and metadata.
    """
    name: str
    type: str
    line_number: int
    end_line: int
    parent: Optional[str] = None
    docstring: Optional[str] = None


@dataclass
class FileDependencies:
    """
    Stores all extracted code elements and their immediate relationships
    for a single Python file before constructing the final graph.
    """
    classes: Dict[str, CodeElement] = field(default_factory=dict)
    functions: Dict[str, CodeElement] = field(default_factory=dict)
    methods: Dict[str, Dict[str, CodeElement]] = field(default_factory=dict)
    inheritance: Dict[str, List[str]] = field(default_factory=dict)
    function_calls: Dict[str, set[str]] = field(default_factory=dict)


# --- Core Parser Logic ---

class DependencyVisitor(ast.NodeVisitor):
    """
    AST visitor to extract elements and their relationships (like definitions,
    inheritance, and function calls) from a single Python file's AST.
    It also captures docstrings for classes and functions/methods.
    """

    def __init__(self):
        """
        Initializes the visitor with a FileDependencies object
        and state variables for the current class and function context.
        """
        self.dependencies = FileDependencies()
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None

    def _get_node_name(self, node: ast.AST) -> str:
        """
        Helper method to extract the name from various AST nodes,
        handling both simple names and attribute access (e.g., 'obj.method').
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value_name = self._get_node_name(node.value)
            return f"{value_name}.{node.attr}" if value_name else node.attr
        return ""

    def _get_end_line(self, node: Union[ast.ClassDef, ast.FunctionDef, ast.AST]) -> int:
        """
        Calculates the precise end line number for an AST node.
        Leverages 'end_lineno' attribute available in Python 3.8+ for precision.
        Falls back to iterating children if 'end_lineno' is not available.
        """
        if hasattr(node, 'end_lineno') and node.end_lineno is not None:
            return node.end_lineno
        elif not node.body:
            return node.lineno
        return max(getattr(child, 'end_lineno', child.lineno) for child in node.body)

    def _get_docstring(self, node: Union[ast.ClassDef, ast.FunctionDef]) -> Optional[str]:
        """
        Extracts the docstring from a given ClassDef or FunctionDef node.
        Docstrings are typically the first expression statement in the body,
        which is a string literal.
        """
        # Ensure the node has a body and it's not empty
        if isinstance(node.body, list) and node.body:
            first_stmt = node.body[0]
            if isinstance(first_stmt, ast.Expr):
                if isinstance(first_stmt.value, ast.Constant) and isinstance(first_stmt.value.value, str):
                    return first_stmt.value.value
        return None

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Visits a ClassDef node to extract class information,
        its inheritance, and its docstring.
        """
        class_name = node.name
        docstring = self._get_docstring(node) # Extract docstring

        self.dependencies.inheritance[class_name] = [self._get_node_name(base) for base in node.bases]
        self.dependencies.classes[class_name] = CodeElement(
            name=class_name,
            type="class",
            line_number=node.lineno,
            end_line=self._get_end_line(node),
            docstring=docstring # Pass the extracted docstring
        )
        self.dependencies.methods[class_name] = {}
        self.current_class = class_name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Visits a FunctionDef node to extract function/method information,
        and its docstring.
        """
        func_name = node.name
        docstring = self._get_docstring(node) # Extract docstring
        is_method = self.current_class is not None
        scope_id = f"{self.current_class}.{func_name}" if is_method else func_name
        self.dependencies.function_calls[scope_id] = set()

        element = CodeElement(
            name=func_name,
            type="method" if is_method else "function",
            line_number=node.lineno,
            end_line=self._get_end_line(node),
            parent=self.current_class,
            docstring=docstring
        )
        if is_method:
            self.dependencies.methods[self.current_class][func_name] = element
        else:
            self.dependencies.functions[func_name] = element

        self.current_function = func_name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node: ast.Call):
        """
        Visits a Call node to record function/method calls made from
        the current function or method scope.
        """

        if self.current_function:
            caller_scope = f"{self.current_class}.{self.current_function}" if self.current_class else self.current_function
            callee_name = self._get_node_name(node.func)
            if callee_name:
                self.dependencies.function_calls[caller_scope].add(callee_name)
        self.generic_visit(node)


class Parser:
    """
    Parses a Python project directory to build a graph of nodes
    representing code elements and their relationships.
    """

    def __init__(self, path: Path):
        """
        Initializes the parser with the project root path.
        """
        self.path = path
        self.nodes: Dict[str, Node] = {}
        self.parse_errors: List[str] = []
        if not self.path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {self.path}")

    def _parse_file(self, file_path: Path) -> Optional[FileDependencies]:
        """
        Parses a single Python file to extract its dependencies using DependencyVisitor.
        Handles potential parsing errors.
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            visitor = DependencyVisitor()
            visitor.visit(tree)
            return visitor.dependencies
        except Exception as e:
            self.parse_errors.append(f"Error parsing {file_path}: {e}")
            return None

    def parse(self):
        """
        Parses all Python files within the specified project path
        and builds the complete node graph in two passes.
        """
        all_deps: Dict[str, FileDependencies] = {}
        python_files = [f for f in self.path.rglob("*.py") if f.is_file()]

        for file_path in python_files:
            relative_path_str = str(file_path.relative_to(self.path))
            file_deps = self._parse_file(file_path)
            if not file_deps:
                continue #
            all_deps[relative_path_str] = file_deps

            module_docstring = None
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content, filename=str(file_path))
                module_docstring = ast.get_docstring(tree)
            except Exception:
                pass

            with open(file_path, 'r', encoding='utf-8') as f:
                line_count = len(f.readlines())
            meta = MetaInfo(path=relative_path_str, start_line=1, end_line=line_count, docstring=module_docstring)
            self.nodes[relative_path_str] = Node(_type=NodeType.FILE, meta=meta, relationships=[])

            for name, elem in file_deps.classes.items():
                meta = MetaInfo(path=relative_path_str, start_line=elem.line_number, end_line=elem.end_line, docstring=elem.docstring)
                self.nodes[name] = Node(_type=NodeType.CLASS, meta=meta, relationships=[])

            if 'FUNCTION' in {member.name for member in NodeType}:
                for name, elem in file_deps.functions.items():
                    # Use docstring from the CodeElement
                    meta = MetaInfo(path=relative_path_str, start_line=elem.line_number, end_line=elem.end_line, docstring=elem.docstring)
                    self.nodes[name] = Node(_type=NodeType.FUNCTION, meta=meta, relationships=[])

            for c_name, methods in file_deps.methods.items():
                for m_name, elem in methods.items():
                    method_id = f"{c_name}.{m_name}"
                    meta = MetaInfo(path=relative_path_str, start_line=elem.line_number, end_line=elem.end_line, docstring=elem.docstring)
                    self.nodes[method_id] = Node(_type=NodeType.METHOD, meta=meta, relationships=[])

        for file_path_str, deps in all_deps.items():
            file_node = self.nodes.get(file_path_str)
            if not file_node:
                continue #

            for name in list(deps.classes.keys()) + list(deps.functions.keys()):
                defined_node = self.nodes.get(name)
                if defined_node:
                    rel = Relationship(relation_type=RelationshipType.DEFINE, parent=file_node, node=defined_node)
                    file_node.relationships.append(rel)

            for c_name, methods in deps.methods.items():
                class_node = self.nodes.get(c_name)
                if not class_node:
                    continue
                for m_name in methods.keys():
                    method_node = self.nodes.get(f"{c_name}.{m_name}")
                    if method_node:
                        rel = Relationship(relation_type=RelationshipType.DEFINE, parent=class_node, node=method_node)
                        class_node.relationships.append(rel)

            if 'INHERIT' in {member.name for member in RelationshipType}:
                for c_name, bases in deps.inheritance.items():
                    class_node = self.nodes.get(c_name)
                    if class_node:
                        for base_name in bases:
                            base_node = self.nodes.get(base_name)
                            if base_node:
                                rel = Relationship(relation_type=RelationshipType.INHERIT, parent=class_node,
                                                   node=base_node)
                                class_node.relationships.append(rel)

            for caller_id, callees in deps.function_calls.items():
                caller_node = self.nodes.get(caller_id)
                if caller_node:
                    for callee_id in callees:
                        callee_node = self.nodes.get(callee_id)
                        if callee_node:
                            rel = Relationship(relation_type=RelationshipType.USE, parent=caller_node, node=callee_node)
                            caller_node.relationships.append(rel)

    def print_node_graph(self):
        """
        Prints a human-readable representation of the generated node graph,
        including docstrings.
        """
        temp_node_to_id_for_printing = {id(v): k for k, v in self.nodes.items()}

        for node_id, node in sorted(self.nodes.items()):
            print(f"\n--- Node: {node_id} ({node._type.value}) ---")
            print(f"  Path: {node.meta.path}, Lines: {node.meta.start_line}-{node.meta.end_line}")
            if node.meta.docstring:
                display_docstring = node.meta.docstring.strip()
                if len(display_docstring) > 100:
                    display_docstring = display_docstring[:97] + "..."
                print(f"  Docstring: \"{display_docstring}\"")
            else:
                print(f"  Docstring: N/A")

            if node.relationships:
                print("  Relationships:")
                for rel in sorted(node.relationships, key=lambda r: (r.relation_type.value, id(r.node))):
                    target_id = temp_node_to_id_for_printing.get(id(rel.node), "Unknown Node")
                    print(f"    - {rel.relation_type.value:<8} -> {target_id} ({rel.node._type.value})")


if __name__ == "__main__":
    # Example usage: Ensure you have a directory named 'syntatic-1'
    # in the same location as this script, containing Python files.
    # For example:
    # syntatic-1/
    #   my_module.py
    #   my_package/
    #     __init__.py
    #     utils.py
    #     my_class.py
    parser = Parser(pathlib.Path("syntatic-1"))
    parser.parse()

    print("\n✅ Parsing complete. Node graph generated.")
    parser.print_node_graph()

    if parser.parse_errors:
        print("\n--- PARSE ERRORS ---")
        for error in parser.parse_errors:
            print(error)
