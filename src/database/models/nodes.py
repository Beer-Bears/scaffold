from neomodel import RelationshipFrom as rFrom
from neomodel import RelationshipTo as rTO
from neomodel import StringProperty, StructuredNode

from src.database.models.mixins import ObjectMetaMixin
from src.generator.graph_types import NodeType as NT
from src.generator.graph_types import RelationshipType as RT


class FunctionNode(StructuredNode, ObjectMetaMixin):
    # DEFINE
    defines_classes = rTO(NT.CLASS, RT.DEFINE)
    defines_methods = rTO(NT.FUNCTION, RT.DEFINE)

    defined_in_file = rFrom(NT.FILE, RT.DEFINE)
    defined_in_class = rFrom(NT.CLASS, RT.DEFINE)

    # USE
    uses_classes = rTO(NT.CLASS, RT.USE)
    uses_methods = rTO(NT.FUNCTION, RT.USE)

    used_by_methods = rFrom(NT.FUNCTION, RT.USE)
    used_by_classes = rFrom(NT.CLASS, RT.USE)
    used_by_files = rFrom(NT.FILE, RT.USE)


class ClassNode(StructuredNode, ObjectMetaMixin):
    # DEFINE
    defined_in_file = rFrom(NT.FILE, RT.DEFINE)
    defines_methods = rTO(NT.FUNCTION, RT.DEFINE)
    defines_classes = rTO(NT.CLASS, RT.DEFINE)

    # USE
    uses_classes = rTO(NT.CLASS, RT.USE)
    uses_methods = rTO(NT.FUNCTION, RT.USE)

    used_by_classes = rFrom(NT.CLASS, RT.USE)
    used_by_methods = rFrom(NT.FUNCTION, RT.USE)
    used_by_files = rFrom(NT.FILE, RT.USE)


class FileNode(StructuredNode, ObjectMetaMixin):
    path = StringProperty(unique_index=True, required=True)

    # DEFINE
    defines_classes = rTO(NT.CLASS, RT.DEFINE)
    defines_methods = rTO(NT.FUNCTION, RT.DEFINE)

    # USE
    uses_files = rTO(NT.FILE, RT.USE)
    uses_classes = rTO(NT.CLASS, RT.USE)
    uses_methods = rTO(NT.FUNCTION, RT.USE)

    # IMPORT
    imports_files = rTO(NT.FILE, RT.IMPORT)
    imports_classes = rTO(NT.CLASS, RT.IMPORT)
    imports_methods = rTO(NT.FUNCTION, RT.IMPORT)


class FolderNode(StructuredNode, ObjectMetaMixin):
    path = StringProperty(unique_index=True, required=True)

    # DEFINE
    defines_folders = rTO(NT.FOLDER, RT.DEFINE)
    defines_files = rTO(NT.FILE, RT.DEFINE)
