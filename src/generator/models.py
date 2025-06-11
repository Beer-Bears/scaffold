from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.generator.types import NodeType, RelationshipType


@dataclass
class Relationship:
    relation_type: RelationshipType
    parent: int
    node: int


@dataclass
class MetaInfo:
    name: str
    path: str
    start_line: int
    end_line: int
    docstring: Optional[str] = None


@dataclass
class Node:
    _type: NodeType
    meta: MetaInfo
    relationships: list[Relationship]
