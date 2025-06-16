from enum import Enum


class NodeType(str, Enum):
    FILE = "FileNode"
    CLASS = "ClassNode"
    METHOD = "MethodNode"


class RelationshipType(str, Enum):
    DEFINE = "DEFINE"
    USE = "USE"
