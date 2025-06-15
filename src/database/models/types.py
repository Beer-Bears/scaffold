from enum import Enum


class NodeType(str, Enum):
    FILE = "FileNode"
    CLASS = "ClassNode"
    METHOD = "MethodNode"


class RelationshipType(str, Enum):
    CONTAINS_CLASS = "CONTAINS_CLASS"
    CONTAINS_METHOD = "CONTAINS_METHOD"
    HAS_METHOD = "HAS_METHOD"
