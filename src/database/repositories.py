from typing import Optional, Type

from neomodel import db

from src.database.models.nodes import FileNode, ClassNode, MethodNode
from src.database.models.types import NodeType

NodeMap = {
    NodeType.FILE: FileNode,
    NodeType.CLASS: ClassNode,
    NodeType.METHOD: MethodNode,
}


class Neo4jRepository:
    def __init__(self):
        self._node_map = NodeMap

    def get_model(self, node_type: NodeType) -> Type:
        return self._node_map[node_type]

    def create_node(self, node_type: NodeType, **props):
        model = self.get_model(node_type)
        return model(**props).save()

    def get_node_by_name(self, node_type: NodeType, name: str):
        model = self.get_model(node_type)
        return model.nodes.get_or_none(name=name)

    def get_node_by_path(self, path: str) -> Optional[FileNode]:
        return FileNode.nodes.get_or_none(path=path)

    def delete_node(self, node_type: NodeType, name: str):
        model = self.get_model(node_type)
        node = model.nodes.get_or_none(name=name)
        if node:
            node.delete()
            return True
        return False

    def connect(self, from_node, rel_name: str, to_node):
        rel = getattr(from_node, rel_name)
        rel.connect(to_node)

    def disconnect(self, from_node, rel_name: str, to_node):
        rel = getattr(from_node, rel_name)
        rel.disconnect(to_node)

    def clear_all(self):
        db.cypher_query("MATCH (n) DETACH DELETE n")
