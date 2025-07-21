import json
from typing import Type, Union

from neomodel import RelationshipFrom, RelationshipTo, StructuredNode

from src.core.config import get_settings
from src.core.vector.index import get_existing_chroma_index
from src.database.models.nodes import ClassNode, FileNode, FolderNode, FunctionNode
from src.generator.graph_types import NodeType, RelationshipType
from src.generator.models import MetaInfo, Node, Relationship

settings = get_settings()


def save_graph_to_db(graph: dict[int, Node]) -> None:
    """
    Сохраняет граф узлов и их связей в базу данных (Neo4j) с использованием neomodel.
    """
    # Шаг 1 — обогатить связи в графе
    enriched_graph = enrich_graph(graph)


    # Шаг 2 — создать все узлы
    id_to_db_node = DbNodes.make_db_nodes(enriched_graph)

    # Шаг 3 — установить связи
    DbRelations.make_db_relations(id_to_db_node, enriched_graph)


ALL_NODE_CLASSES = [FunctionNode, ClassNode, FileNode, FolderNode]


def get_code(path: str, start_line: int, end_line: int) -> str:
    """
    Return part of source code by path, start_line and end_line.
    Lines are 1-indexed, inclusive.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Проверка границ
            if start_line < 1 or end_line > len(lines) or start_line > end_line:
                return f"[Invalid line range: {start_line}-{end_line}]"
            return "".join(lines[start_line - 1 : end_line])
    except FileNotFoundError:
        return f"[File not found: {path}]"
    except Exception as e:
        return f"[Error reading file: {e}]"


def get_node_information(node_name: str) -> str:
    node_instance: Union[FunctionNode, ClassNode, FileNode, FolderNode, None] = None

    # Попытка найти узел среди всех типов
    for NodeCls in ALL_NODE_CLASSES:
        try:
            node_instance = NodeCls.nodes.filter(name=node_name).first()
            break
        except Exception:
            continue

    if not node_instance:
        return f"Node with name '{node_name}' not found."

    # Метаинформация
    meta_info = [
        f"name: {node_instance.name}",
        f"path: {node_instance.path}",
        f"start_line: {node_instance.start_line}",
        f"end_line: {node_instance.end_line}",
        f"docstring: {node_instance.docstring}",
    ]
    meta_block = "\n".join(meta_info)
    # Представление узла
    code_repr = get_code(
        node_instance.path, node_instance.start_line, node_instance.end_line
    )

    # Связи
    relations_block = []
    for attr in dir(node_instance.__class__):
        if attr.startswith("__"):
            continue
        rel_descriptor = getattr(node_instance.__class__, attr)
        if isinstance(rel_descriptor, (RelationshipTo, RelationshipFrom)):
            related = getattr(node_instance, attr)
            try:
                targets = related.all()
                for t in targets:
                    relations_block.append(
                        f"{attr}: {t.__class__.__name__} {getattr(t, 'name', '???')}"
                    )
            except Exception as e:
                relations_block.append(f"{attr}: ERROR - {str(e)}")
    index = get_existing_chroma_index()
    retriever = index.as_retriever(
        similarity_top_k=5, choice_batch_size=5, embed_model=settings.vector.embed_model
    )
    results = retriever.retrieve(f"{node_name}")
    vector_result = ""
    for result in results:
        vector_result += (
            f"source:{result.get_text()} metadata:{json.dumps(result.json())}\n"
        )

    return (
        meta_block
        + "\nSource code:"
        + code_repr
        + "\n------\n"
        + "Relationships:\n"
        + "\n".join(relations_block)
        + "\nVector RAG:\n"
        + vector_result
    )


def get_all_functions() -> str:
    return "\n".join([f"{a.path}:\n{a.name}" for a in list(FunctionNode.nodes)])


def get_all_classes() -> str:
    return "\n".join([f"{a.path}:\n{a.name}" for a in list(ClassNode.nodes)])


def enrich_graph(graph: dict[int, Node]) -> dict[int, Node]:
    """
    Обогащает связи в графе:
     - Добавляет папки
     - Подвязывает дочерние ноды к родителям родителей (надо ли?)
    """
    items = list(graph.items())
    for node_id, node in items:
        if node._type is not NodeType.FILE:
            continue
        path = str(node.meta.path)
        child_id = node_id
        for splits in range(path.count("/"), 0, -1):
            folder = "/".join(path.split("/")[:splits])
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
                child_id = folder_id
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
            case FunctionNode(), ClassNode(), RelationshipType.DEFINE:
                parent.defines_classes.connect(child)
            case FunctionNode(), FunctionNode(), RelationshipType.DEFINE:
                parent.defines_methods.connect(child)

            # USE
            case FileNode(), FileNode(), RelationshipType.USE:
                parent.uses_files.connect(child)
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

            # IMPORT
            case FileNode(), FileNode(), RelationshipType.IMPORT:
                parent.imports_files.connect(child)
            case FileNode(), ClassNode(), RelationshipType.IMPORT:
                parent.imports_classes.connect(child)
            case FileNode(), FunctionNode(), RelationshipType.IMPORT:
                parent.imports_methods.connect(child)

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
