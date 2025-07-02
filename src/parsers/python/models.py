from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from src.generator.graph_types import NodeType, RelationshipType
from src.generator.models import Relationship


@dataclass
class CodeElement:
    """
    Represents a single code element (class, function, method) found in a file.
    Includes details necessary for graph construction and metadata.
    """

    name: str
    type: NodeType
    line_number: int
    end_line: int
    docstring: Optional[str] = None


class FileGraph:
    """
    Stores all extracted code elements and their immediate relationships
    for a single Python file before constructing the final graph.
    """

    def __init__(self, path: str):
        self.path = path
        self.counter = 1

        # A -> 1
        # A.func -> 2
        # A.func.func2 -> 3
        # B -> 4
        # B.func -> 5
        self.id_to_scope: dict[int, str] = {0: ""}
        self.scope_to_id: dict[str, int] = {"": 0}

        # A -> 1
        # func -> 2
        # func2 -> 3
        # B -> 4
        # func -> 5
        self.nodes: dict[int, CodeElement] = {}
        self.relations: dict[int, list[Relationship]] = defaultdict(list)

    def get_scope_id(self, scope_list: list[str]) -> int:
        scope = ".".join(scope_list)
        _id = self.scope_to_id.get(scope, None)
        if _id is None:
            self.scope_to_id[scope] = self.counter
            _id = self.counter
            self.id_to_scope[_id] = scope
            self.counter += 1

        return _id

    def get_name_of_node_in_scope(self, scope_id: int) -> Optional[str]:
        scope = self.id_to_scope.get(scope_id, None)
        if scope is None:
            return None
        return scope.split(".")[-1]

    def add_element(
        self, scope_list: list[str], elem: CodeElement, relation_type: RelationshipType
    ) -> None:
        scope_id = self.get_scope_id(scope_list)
        self.nodes[scope_id] = elem
        parent_id = self.get_parent_id(scope_list)
        # print(scope_id, scope_list, parent_id)
        self.relations[parent_id].append(
            Relationship(relation_type=relation_type, parent=parent_id, node=scope_id)
        )

    def get_parent_id(self, scope_list: list[str]) -> int:
        scope = ".".join(scope_list[:-1])
        _id = self.scope_to_id.get(scope, None)
        assert (
            _id is not None
        ), f"Parent have to exist always: \n{self.scope_to_id}\n{self.id_to_scope}\n {_id} -> {scope}"
        return _id
