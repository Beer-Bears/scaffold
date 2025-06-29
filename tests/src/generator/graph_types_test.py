from src.generator.graph_types import NodeType, RelationshipType


def test_node_type():
    assert hasattr(NodeType, "FILE")
    assert hasattr(NodeType, "CLASS")
    assert hasattr(NodeType, "FUNCTION")


def test_relationship_type():
    assert hasattr(RelationshipType, "DEFINE")
    assert hasattr(RelationshipType, "USE")
