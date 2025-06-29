from enum import Enum


class NodeType(str, Enum):
    FILE = "FileNode"
    CLASS = "ClassNode"
    FUNCTION = "FunctionNode"


class RelationshipType(str, Enum):
    DEFINE = "DEFINE"
    USE = "USE"
