from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo as rTO,
    RelationshipFrom as rFrom
)

from src.database.models.mixins import ObjectMetaMixin
from src.database.models.types import (
    NodeType as NT,
    RelationshipType as RT
)


class MethodNode(StructuredNode, ObjectMetaMixin):
    file = rFrom(
        NT.FILE,
        RT.CONTAINS_CLASS
    )
    parent_class = rFrom(
        NT.CLASS,
        RT.CONTAINS_METHOD
    )


class ClassNode(StructuredNode, ObjectMetaMixin):
    methods = rTO(
        NT.CLASS,
        RT.HAS_METHOD
    )
    file = rFrom(
        NT.FILE,
        RT.CONTAINS_CLASS
    )


class FileNode(StructuredNode):
    path = StringProperty(unique_index=True, required=True)

    classes = rTO(
        NT.CLASS,
        RT.CONTAINS_CLASS
    )
    methods = rTO(
        NT.METHOD,
        RT.CONTAINS_METHOD
    )
