import ast
import pathlib
from pathlib import Path
from typing import Dict, List

from src.generator.graph_types import NodeType
from src.generator.models import MetaInfo, Node, Relationship
from src.ignorer.ignorer import Ignorer
from src.parsers.python.import_node_visitor import ImportNodeVisitor
from src.parsers.python.models import FileGraph
from src.parsers.python.node_visitor import NodeVisitor


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
        self.nodes: Dict[int, Node] = {}
        self.node_id_map: Dict[str, int] = {}
        self.parse_errors: List[str] = []
        if not self.path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {self.path}")

    def _parse_file(self, file_path: Path) -> FileGraph:
        """
        Parses a single Python file to extract its dependencies using DependencyVisitor.
        Handles potential parsing errors.
        """
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
        visitor = NodeVisitor(file_path)
        visitor.visit(tree)
        file = visitor.file
        print("-" * 100)
        print(f"[Parse Imports] {file_path}")
        print()

        # file docstring
        tree = ast.parse(content, filename=str(file_path))
        module_docstring = ast.get_docstring(tree)
        file.docstring = module_docstring
        # pprint(file.nodes)
        # pprint(file.relations)
        # file.relations.pop(0)
        return file

    def parse(self):
        """
        Parses all Python files within the specified project path
        and builds the complete node graph in two passes.
        """
        file_paths = [f for f in self.path.rglob("*.py") if f.is_file()]
        for file_path in file_paths:
            ignorer = Ignorer(file_path.parent, self.path)
            if ignorer.is_ignore(file_path):
                continue

            file = self._parse_file(file_path)
            if not file:
                continue

            # pprint(file)

            with open(file_path, "r", encoding="utf-8") as f:
                line_count = len(f.readlines())
            meta = MetaInfo(
                name=f.name,
                path=str(file_path),
                start_line=1,
                end_line=line_count,
                docstring="",  # todo
            )
            file_node = Node(_type=NodeType.FILE, meta=meta, relationships=[])
            file_node_id = len(self.nodes) + 1
            self.nodes[file_node_id] = file_node
            self.node_id_map[str(file_path)] = file_node_id

            element_id_to_node_id = {0: file_node_id}
            node_id_to_element_id = {file_node_id: 0}
            for elem_id, elem in file.nodes.items():
                meta = MetaInfo(
                    name=elem.name,
                    path=str(file_path),
                    start_line=elem.line_number,
                    end_line=elem.end_line,
                    docstring=elem.docstring,
                )
                node = Node(_type=elem.type, meta=meta, relationships=[])
                node_id = len(self.nodes) + 1
                assert node_id not in self.nodes.keys()
                self.nodes[node_id] = node
                element_id_to_node_id[elem_id] = node_id
                node_id_to_element_id[node_id] = elem_id

            for elem_id, relations in file.relations.items():
                for relation in relations:
                    self.nodes[element_id_to_node_id[elem_id]].relationships.append(
                        Relationship(
                            relation_type=relation.relation_type,
                            parent=element_id_to_node_id[elem_id],
                            node=element_id_to_node_id[relation.node],
                        )
                    )

        for file_path in file_paths:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))
            visitor = ImportNodeVisitor(str(file_path), self.nodes)
            visitor.visit(tree)
            self.nodes = visitor.nodes

    def print_node_graph(self):
        """
        Prints a human-readable representation of the generated node graph,
        including docstrings.
        """
        for node_unique_id, node in sorted(
            self.nodes.items(), key=lambda item: item[0]
        ):  # Sort by unique ID

            print(
                f"\n--- Node: {node.meta.name} (ID: {node_unique_id}) ({node._type.value}) ---"
            )
            print(
                f"  Path: {node.meta.path}, Lines: {node.meta.start_line}-{node.meta.end_line}"
            )
            if node.meta.docstring:
                display_docstring = node.meta.docstring.strip()
                if len(display_docstring) > 100:
                    display_docstring = display_docstring[:97] + "..."
                print(f'  Docstring: "{display_docstring}"')
            else:
                print("  Docstring: N/A")

            if node.relationships:
                print("  Relationships:")
                for rel in sorted(
                    node.relationships, key=lambda r: (r.relation_type.value, r.node)
                ):
                    print(
                        f"    - {rel.relation_type.value:<8} {rel.parent} -> (ID: {rel.node}) ({self.nodes[rel.node]._type.value})"
                    )


if __name__ == "__main__":
    parser = Parser(pathlib.Path("codebase"))
    parser.parse()

    print("\n✅ Parsing complete. Node graph generated.")
    # parser.print_node_graph()

    if parser.parse_errors:
        print("\n--- PARSE ERRORS ---")
        for error in parser.parse_errors:
            print(error)
