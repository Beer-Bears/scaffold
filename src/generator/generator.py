from typing import Type

from neomodel import StructuredNode

from src.database.models.nodes import ClassNode, FileNode, MethodNode
from src.generator.graph_types import NodeType, RelationshipType
from src.generator.models import Node, Relationship


def save_graph_to_db(graph: dict[int, Node]) -> None:
    """
    Сохраняет граф узлов и их связей в базу данных (Neo4j) с использованием neomodel.
    """

    # Шаг 1 — создать все узлы
    id_to_db_node = DbNodes.make_db_nodes(graph)

    # Шаг 2 — установить связи
    DbRelations.make_db_relations(id_to_db_node, graph)


class DbNodes:

    @staticmethod
    def make_db_nodes(graph: dict[int, Node]) -> dict[int, StructuredNode]:
        """
        Записывает ноды в бд
        :return: dict id -> db_node
        """
        id_to_db_node: dict[int, StructuredNode] = {}

        for node_id, node in graph.items():
            Model = DbNodes.node_type_to_model(node._type)
            if not Model:
                print(
                    f"⚠️ Пропущен узел {node_id} с неподдерживаемым типом {node._type}"
                )
                continue

            db_node = Model(
                name=node.meta.name,
                path=node.meta.path,
                start_line=node.meta.start_line,
                end_line=node.meta.end_line,
                docstring=node.meta.docstring,
            )
            db_node.save()
            id_to_db_node[node_id] = db_node

        return id_to_db_node

    @staticmethod
    def node_type_to_model(_type: NodeType) -> Type[StructuredNode]:
        """
        Сопоставление NodeType -> StructuredNode (neomodel)
        """
        models = {
            NodeType.FILE: FileNode,
            NodeType.CLASS: ClassNode,
            NodeType.METHOD: MethodNode,
        }

        model = models.get(_type)
        if model is None:
            raise ValueError(f"Unsupported NodeType: {_type}")
        return model


class DbRelations:

    @staticmethod
    def make_db_relations(
        id_to_db_node: dict[int, StructuredNode], graph: dict[int, Node]
    ):
        """
        Устанавливает связи в БД

        Для каждой db_node:
         1. Вытаскивает связи из графа в виде (RelationshipType -> StructuredNode)
         2. Записывает связи в БД
        """
        for node_id, db_node in id_to_db_node.items():
            db_node_relationship = DbRelations.relations_of_db_node(
                id_to_db_node, graph[node_id].relationships
            )

            DbRelations.make_db_relations_for_node(db_node, db_node_relationship)

    @staticmethod
    def relations_of_db_node(
        db_nodes: dict[int, StructuredNode], graph_relationships: list[Relationship]
    ) -> list[tuple[RelationshipType, StructuredNode]]:
        return [(rel.relation_type, db_nodes[rel.node]) for rel in graph_relationships]

    @staticmethod
    def make_db_relation_for_node(
        parent: StructuredNode, child: StructuredNode, rel: RelationshipType
    ):
        match parent, child, rel:
            # DEFINE
            case FileNode(), ClassNode(), RelationshipType.DEFINE:
                parent.defines_classes.connect(child)
            case FileNode(), MethodNode(), RelationshipType.DEFINE:
                parent.defines_methods.connect(child)

            case ClassNode(), MethodNode(), RelationshipType.DEFINE:
                parent.defines_methods.connect(child)

            # USE
            case FileNode(), ClassNode(), RelationshipType.USE:
                parent.uses_classes.connect(child)
            case FileNode(), MethodNode(), RelationshipType.USE:
                parent.uses_methods.connect(child)

            case ClassNode(), ClassNode(), RelationshipType.USE:
                parent.uses_classes.connect(child)
            case ClassNode(), MethodNode(), RelationshipType.USE:
                parent.uses_methods.connect(child)

            case MethodNode(), ClassNode(), RelationshipType.USE:
                parent.uses_classes.connect(child)
            case MethodNode(), MethodNode(), RelationshipType.USE:
                parent.uses_methods.connect(child)

            case _:
                raise ValueError(
                    f"Unsupported combination: {type(parent).__name__} -> {type(child).__name__} with relation {rel}"
                )

    @staticmethod
    def make_db_relations_for_node(
        db_node: StructuredNode,
        relations: list[tuple[RelationshipType, StructuredNode]],
    ):
        for rel, db_target in relations:
            DbRelations.make_db_relation_for_node(db_node, db_target, rel)
