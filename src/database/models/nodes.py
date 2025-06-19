from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo as rTO,
    RelationshipFrom as rFrom
)
from src.database.models.mixins import ObjectMetaMixin
from src.generator.types import NodeType as NT, RelationshipType as RT


class MethodNode(StructuredNode, ObjectMetaMixin):
    # DEFINE
    defined_in_file = rFrom(NT.FILE, RT.DEFINE)
    defined_in_class = rFrom(NT.CLASS, RT.DEFINE)

    # USE
    uses_classes = rTO(NT.CLASS, RT.USE)
    uses_methods = rTO(NT.METHOD, RT.USE)

    used_by_methods = rFrom(NT.METHOD, RT.USE)
    used_by_classes = rFrom(NT.CLASS, RT.USE)
    used_by_files = rFrom(NT.FILE, RT.USE)


class ClassNode(StructuredNode, ObjectMetaMixin):
    # DEFINE
    defined_in_file = rFrom(NT.FILE, RT.DEFINE)
    defines_methods = rTO(NT.METHOD, RT.DEFINE)

    # USE
    uses_classes = rTO(NT.CLASS, RT.USE)
    uses_methods = rTO(NT.METHOD, RT.USE)

    used_by_classes = rFrom(NT.CLASS, RT.USE)
    used_by_methods = rFrom(NT.METHOD, RT.USE)
    used_by_files = rFrom(NT.FILE, RT.USE)


class FileNode(StructuredNode, ObjectMetaMixin):
    path = StringProperty(unique_index=True, required=True)

    # DEFINE
    defines_classes = rTO(NT.CLASS, RT.DEFINE)
    defines_methods = rTO(NT.METHOD, RT.DEFINE)

    # USE
    uses_classes = rTO(NT.CLASS, RT.USE)
    uses_methods = rTO(NT.METHOD, RT.USE)
