"""Generate Python entity classes from a YAML schema.

Parses the YAML output of ``GraphStore.schema_yaml()`` and generates
Python source code with class definitions for every label, relationship,
and weak relation found in the schema.

Example usage::

    from drm.networkx_graph import NetworkXGraph
    from drm.schema_gen import generate_classes, generate_file

    g = NetworkXGraph(persistence_path="my_graph.pkl")
    source = generate_classes(g.schema_yaml("my_db"))

    # Or write directly to a file:
    generate_file(g, "my_db", output_dir="entities/")

Output structure::

    from drm.base import Node, WeakNode, Relation, WeakRelation

    class Character(Node):
        \"\"\"Auto-generated from schema.\"\"\"

        def __init__(self, pk, **kwargs):
            super().__init__(pk=pk, main_label="Character", **kwargs)
            self.house = kwargs.get("house", "")
            self.name = kwargs.get("name", "")

    class Section(WeakNode):
        \"\"\"Auto-generated from schema.\"\"\"

        def __init__(self, parent, **kwargs):
            super().__init__(parent=parent, main_label="Section",
                             parent_relation="HAS_SECTION", **kwargs)
            self.title = kwargs.get("title", "")

    class Knows(Relation):
        \"\"\"Auto-generated from schema.\"\"\"

        def __init__(self, src, dst, **kwargs):
            super().__init__(src=src, dst=dst, rel_type="KNOWS", **kwargs)

    class HasSection(WeakRelation):
        \"\"\"Auto-generated from schema.\"\"\"

        def __init__(self, src, dst, **kwargs):
            super().__init__(src=src, dst=dst, rel_type="HAS_SECTION",
                             propagate=True, **kwargs)
"""

from __future__ import annotations

import datetime
import os
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from .networkx_graph import NetworkXGraph


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_classes(yaml_source: str) -> str:
    """Generate Python entity classes from a YAML schema string.

    Args:
        yaml_source: The YAML string returned by
            ``GraphStore.schema_yaml(db_name)`` or ``rdf_to_yaml()``.

    Returns:
        A Python source string containing all generated classes.
    """
    if yaml is None:
        raise ImportError(
            "PyYAML is required for schema generation. "
            "Install it with: pip install pyyaml"
        )

    data = yaml.safe_load(yaml_source)
    lines: List[str] = []

    # Header
    lines.append('"""Auto-generated entity classes from schema."""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any, Dict, List, Optional")
    lines.append("")
    lines.append("from drm.base import Node, WeakNode, Relation, WeakRelation")
    lines.append("")
    lines.append("")

    # ── Node / WeakNode classes ────────────────────────────────────
    labels = data.get("labels", {}) or {}
    for label_name in sorted(labels):
        info = labels[label_name]
        base_class = info.get("base_class", "Node")
        props = info.get("properties", {}) or {}
        class_name = info.get("class_name", label_name)
        primary_key: List[str] = info.get("primary_key", []) or []
        doc = info.get("doc", f"Auto-generated entity class.")

        if base_class == "WeakNode":
            lines.append(_generate_weaknode_class(
                class_name, label_name, props,
                info.get("parent"),
                info.get("parent_relation"),
                primary_key,
                doc,
            ))
        else:
            lines.append(_generate_node_class(
                class_name, label_name, props,
                primary_key,
                doc,
            ))

    # ── Regular Relation classes ───────────────────────────────────
    rels = data.get("relationships", {}) or {}
    for rel_name in sorted(rels):
        info = rels[rel_name]
        # Skip if this is a WeakRelation (already in weak_relations)
        wr = data.get("weak_relations", {}) or {}
        if rel_name in wr:
            continue
        class_name = info.get("class_name", rel_name)
        lines.append(_generate_relation_class(
            class_name, rel_name, info.get("properties", {}) or {},
        ))

    # ── WeakRelation classes ───────────────────────────────────────
    wrs = data.get("weak_relations", {}) or {}
    for rel_name in sorted(wrs):
        info = wrs[rel_name]
        class_name = info.get("class_name", rel_name)
        propagate = info.get("propagate", True)
        lines.append(_generate_weakrelation_class(
            class_name, rel_name, propagate,
        ))

    return "\n".join(lines) + "\n"


def generate_file(
    graph: NetworkXGraph,
    db_name: str,
    output_dir: str,
    filename: Optional[str] = None,
) -> str:
    """Generate Python entity classes and write them to a file.

    Args:
        graph: A graph store instance (NetworkXGraph or Neo4jGraph).
        db_name: Database name used for schema introspection.
        output_dir: Directory where the .py file will be written.
        filename: Output filename (default: ``entities_{db_name}.py``).

    Returns:
        The absolute path to the generated file.
    """
    if filename is None:
        filename = f"entities_{db_name}.py"

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, filename)

    yaml_source = graph.schema_yaml(db_name)
    source = generate_classes(yaml_source)

    with open(out_path, "w") as f:
        f.write(source)

    return os.path.abspath(out_path)


# ---------------------------------------------------------------------------
# Class generators
# ---------------------------------------------------------------------------


def _generate_node_class(
    class_name: str,
    label: str,
    props: Dict[str, str],
    primary_key: List[str],
    doc: str,
) -> str:
    """Generate a Node subclass."""
    lines: List[str] = []
    lines.append(f"class {class_name}(Node):")
    lines.append(f'    """{doc}."""')
    lines.append("")

    # pk is optional when no primary_key defined
    pk_type = "Dict[str, Any]" if primary_key else "Optional[Dict[str, Any]]"
    pk_default = f" = None" if not primary_key else ""
    lines.append(f"    def __init__(self, pk: {pk_type}{pk_default}, **kwargs: Any) -> None:")
    lines.append(f'        """Initialize a {class_name} node.')
    lines.append("")
    lines.append(f"        Args:")
    if primary_key:
        lines.append(f"            pk: Primary key dict with fields: {', '.join(primary_key)}.")
    else:
        lines.append(f"            pk: Optional primary key dict. When not provided, the backend assigns an ID.")
    lines.append(f"            **kwargs: Additional properties and attributes.")
    lines.append(f"        \"\"\"")

    # Call super().__init__
    init_kwargs = [f"pk=pk", f'main_label="{label}"']
    lines.append("        super().__init__(" + ", ".join(init_kwargs) + ", **kwargs)")

    # Set properties
    for prop_name in sorted(props):
        lines.append(f"        self.{prop_name} = kwargs.get(\"{prop_name}\", {props[prop_name]!r})")

    return "\n".join(lines)


def _generate_weaknode_class(
    class_name: str,
    label: str,
    props: Dict[str, str],
    parent_label: Optional[str],
    parent_relation: Optional[str],
    primary_key: List[str],
    doc: str,
) -> str:
    """Generate a WeakNode subclass."""
    lines: List[str] = []
    lines.append(f"class {class_name}(WeakNode):")
    lines.append(f'    """{doc}."""')
    lines.append("")
    lines.append(f"    def __init__(self, parent: Node, **kwargs: Any) -> None:")
    lines.append(f'        """Initialize a {class_name} weak node.')
    lines.append("")
    lines.append(f"        Args:")
    lines.append(f"            parent: The parent {parent_label or 'Node'} instance.")
    lines.append(f"            **kwargs: Additional properties and attributes.")
    lines.append(f"        \"\"\"")

    # Call super().__init__
    init_kwargs = [f"parent=parent", f'main_label="{label}"']
    if parent_relation:
        init_kwargs.append(f'parent_relation="{parent_relation}"')
    lines.append("        super().__init__(" + ", ".join(init_kwargs) + ", **kwargs)")

    # Set properties
    for prop_name in sorted(props):
        lines.append(f"        self.{prop_name} = kwargs.get(\"{prop_name}\", {props[prop_name]!r})")

    return "\n".join(lines)


def _generate_relation_class(
    class_name: str,
    rel_type: str,
    props: Dict[str, str],
) -> str:
    """Generate a Relation subclass."""
    lines: List[str] = []
    lines.append(f"class {class_name}(Relation):")
    lines.append(f'    """Auto-generated relation class."""')
    lines.append("")
    lines.append(f"    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:")
    lines.append(f'        """Initialize a {class_name} relation.')
    lines.append("")
    lines.append(f"        Args:")
    lines.append(f"            src: Source node.")
    lines.append(f"            dst: Destination node.")
    lines.append(f"            **kwargs: Edge properties.")
    lines.append(f"        \"\"\"")

    init_kwargs = [f"src=src", f"dst=dst", f'rel_type="{rel_type}"']
    lines.append("        super().__init__(" + ", ".join(init_kwargs) + ", **kwargs)")

    # Set properties
    for prop_name in sorted(props):
        lines.append(f"        self.{prop_name} = kwargs.get(\"{prop_name}\", {props[prop_name]!r})")

    return "\n".join(lines)


def _generate_weakrelation_class(
    class_name: str,
    rel_type: str,
    propagate: bool = True,
) -> str:
    """Generate a WeakRelation subclass.

    Args:
        class_name: The name of the class to generate.
        rel_type: The relation type (e.g. ``"HAS_PAGE"``).
        propagate: Whether the relation carries the ``_propagate=TRUE``
            flag for cascade delete (default ``True``).
    """
    lines: List[str] = []
    lines.append(f"class {class_name}(WeakRelation):")
    lines.append(f'    """Auto-generated weak relation class.')
    lines.append(f'')
    lines.append(f'    Propagate: {propagate}.')
    lines.append(f'    """')
    lines.append("")
    lines.append(f"    def __init__(self, src: Node, dst: Node, **kwargs: Any) -> None:")
    lines.append(f'        """Initialize a {class_name} weak relation.')
    lines.append("")
    lines.append(f"        Args:")
    lines.append(f"            src: Source (parent) node.")
    lines.append(f"            dst: Destination (child) node.")
    lines.append(f"            propagate: Override the default propagation flag.")
    lines.append(f"            **kwargs: Edge properties.")
    lines.append(f"        \"\"\"")

    init_kwargs = [f"src=src", f"dst=dst", f'rel_type="{rel_type}"']
    if propagate:
        init_kwargs.append(f"propagate={propagate}")
    lines.append("        super().__init__(" + ", ".join(init_kwargs) + ", **kwargs)")

    return "\n".join(lines)
