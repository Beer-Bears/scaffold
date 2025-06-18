from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class CodeElement:
    """
    Represents a single code element (class, function, method) found in a file.
    Includes details necessary for graph construction and metadata.
    """
    name: str
    type: str
    line_number: int
    end_line: int
    parent: Optional[str] = None
    docstring: Optional[str] = None


@dataclass
class FileDependencies:
    """
    Stores all extracted code elements and their immediate relationships
    for a single Python file before constructing the final graph.
    """
    classes: Dict[str, CodeElement] = field(default_factory=dict)
    functions: Dict[str, CodeElement] = field(default_factory=dict)
    methods: Dict[str, Dict[str, CodeElement]] = field(default_factory=dict)
    inheritance: Dict[str, List[str]] = field(default_factory=dict)
    function_calls: Dict[str, set[str]] = field(default_factory=dict)
