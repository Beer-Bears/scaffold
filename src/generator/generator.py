from pprint import pprint
from typing import Type

from neomodel import StructuredNode

from src.database.models.nodes import ClassNode, FileNode, FolderNode, FunctionNode
from src.generator.graph_types import NodeType, RelationshipType
from src.generator.models import MetaInfo, Node, Relationship


def save_graph_to_db(graph: dict[int, Node]) -> None:
    """
    Сохраняет граф узлов и их связей в базу данных (Neo4j) с использованием neomodel.
    """
    # Шаг 1 — обогатить связи в графе
    enriched_graph = enrich_graph(graph)

    pprint(enriched_graph)

    # Шаг 2 — создать все узлы
    id_to_db_node = DbNodes.make_db_nodes(enriched_graph)

    # Шаг 3 — установить связи
    DbRelations.make_db_relations(id_to_db_node, enriched_graph)


def enrich_graph(graph: dict[int, Node]) -> dict[int, Node]:
    """
    Обогащает связи в графе:
     - Добавляет папки
     - Подвязывает дочерние ноды к родителям родителей (надо ли?)
    """
    # todo split algorithm to functions
    print("start enrich_graph")
    items = list(graph.items())
    for node_id, node in items:
        print("[enrich_graph]", node_id, node)
        if node._type is not NodeType.FILE:
            continue
        print("[enrich_graph]", node_id, node)
        path = str(node.meta.path)
        child_id = node_id
        print("[enrich_graph] Count /:", path.count("/"))
        print("[enrich_graph]", list(range(path.count("/"), 0, -1)))
        for splits in range(path.count("/"), 0, -1):
            print("[enrich_graph]", splits)
            folder = "/".join(path.split("/")[:splits])
            print("[enrich_graph]", folder, child_id)
            if folder not in [x.meta.name for x in graph.values()]:
                folder_id = len(graph.items()) + 1
                graph[folder_id] = Node(  # todo shift creation out to a function
                    _type=NodeType.FOLDER,
                    meta=MetaInfo(
                        name=folder,
                        path=folder,
                        start_line=0,
                        end_line=0,
                    ),
                    relationships=[
                        Relationship(RelationshipType.DEFINE, folder_id, child_id)
                    ],
                )
                print("[enrich_graph] New folder: ", folder_id, graph[folder_id])
                child_id = folder_id
                print("[enrich_grap]", child_id)
            else:
                folder_id = [
                    folder_id for folder_id, f in graph.items() if f.meta.name == folder
                ][
                    0
                ]  # todo create reverse map for finding folder_id by folder name
                graph[folder_id].relationships += [
                    Relationship(RelationshipType.DEFINE, folder_id, child_id)
                ]
                child_id = folder_id
    print("end enrich_graph")
    return graph


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
            NodeType.FOLDER: FolderNode,
            NodeType.FILE: FileNode,
            NodeType.CLASS: ClassNode,
            NodeType.FUNCTION: FunctionNode,
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
        # pprint(id_to_db_node)
        for node_id, db_node in id_to_db_node.items():
            # print(node_id, db_node)
            db_node_relationship = DbRelations.relations_of_db_node(
                id_to_db_node, graph[node_id].relationships
            )
            # pprint(db_node_relationship)
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
        # print(parent, child, rel)
        match parent, child, rel:
            # DEFINE
            case FolderNode(), FolderNode(), RelationshipType.DEFINE:
                parent.defines_folders.connect(child)
            case FolderNode(), FileNode(), RelationshipType.DEFINE:
                parent.defines_files.connect(child)
            case FileNode(), ClassNode(), RelationshipType.DEFINE:
                parent.defines_classes.connect(child)
            case FileNode(), FunctionNode(), RelationshipType.DEFINE:
                parent.defines_methods.connect(child)
            case ClassNode(), FunctionNode(), RelationshipType.DEFINE:
                parent.defines_methods.connect(child)
            case ClassNode(), ClassNode(), RelationshipType.DEFINE:
                parent.defines_classes.connect(child)
            case FunctionNode(), FunctionNode(), RelationshipType.DEFINE:
                parent.defines_methods.connect(child)

            # USE
            case FileNode(), ClassNode(), RelationshipType.USE:
                parent.uses_classes.connect(child)
            case FileNode(), FunctionNode(), RelationshipType.USE:
                parent.uses_methods.connect(child)

            case ClassNode(), ClassNode(), RelationshipType.USE:
                parent.uses_classes.connect(child)
            case ClassNode(), FunctionNode(), RelationshipType.USE:
                parent.uses_methods.connect(child)

            case FunctionNode(), ClassNode(), RelationshipType.USE:
                parent.uses_classes.connect(child)
            case FunctionNode(), FunctionNode(), RelationshipType.USE:
                parent.uses_methods.connect(child)

            case _:
                raise ValueError(
                    f"Unsupported combination:\n"
                    f"{type(parent)} -{rel}-> {type(child)}\n"
                    f"{parent} -> {child} with relation {rel}"
                )

    @staticmethod
    def make_db_relations_for_node(
        db_node: StructuredNode,
        relations: list[tuple[RelationshipType, StructuredNode]],
    ):
        for rel, db_target in relations:
            DbRelations.make_db_relation_for_node(db_node, db_target, rel)
