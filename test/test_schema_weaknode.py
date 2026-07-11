"""Tests for WeakNode hierarchy detection in schema_yaml().

WeakNodes are inferred from composite PKs: if label A's PK fields
are a superset of label B's PK fields, then A is a child of B.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest

try:
    import yaml
except ImportError:
    yaml = None

from drm.base import Node, Relation, WeakNode
from drm.networkx_graph import NetworkXGraph


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_hierarchy_graph() -> NetworkXGraph:
    """Create a NetworkXGraph with WeakNode hierarchies."""
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "hierarchy.pkl")
    g = NetworkXGraph(persistence_path=path)
    g._temp_path = tmp

    # Document (root)
    doc = Node(pk={"id": 1}, main_label="Document", name="Informe")
    g.insertNode(doc, replace=True)

    # Section (WeakNode of Document)
    sec1 = WeakNode(pk={"title": "Introducció"}, main_label="Section",
                    parent=doc, parent_relation="HAS_SECTION")
    g.insertNode(sec1, replace=True)
    sec2 = WeakNode(pk={"title": "Desenvolupament"}, main_label="Section",
                    parent=doc, parent_relation="HAS_SECTION")
    g.insertNode(sec2, replace=True)

    # Page (WeakNode of Section)
    page1 = WeakNode(pk={"number": 1}, main_label="Page",
                     parent=sec1, parent_relation="HAS_PAGE")
    g.insertNode(page1, replace=True)

    # Character (standalone, NOT a WeakNode)
    g.insertNode(Node(pk={"name": "Jon Snow"}, main_label="Character",
                      house="Stark"), replace=True)

    return g


# ---------------------------------------------------------------------------
# WeakNode hierarchy detection
# ---------------------------------------------------------------------------


class WeakNodeDetectionTest(unittest.TestCase):
    """Tests for WeakNode hierarchy detection via composite PKs."""

    def setUp(self) -> None:
        self.graph = _make_hierarchy_graph()

    def tearDown(self) -> None:
        path = getattr(self.graph, "_temp_path", None)
        try:
            self.graph.close()
        except Exception:
            pass
        if path and os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

    def test_section_is_weaknode(self) -> None:
        """Section has parent=Document and base_class=WeakNode."""
        result = self.graph.schema_yaml("test")
        self.assertIn("base_class: WeakNode", result)
        self.assertIn("parent: Document", result)
        self.assertIn("parent_relation: HAS_SECTION", result)

    def test_page_is_weaknode(self) -> None:
        """Page has parent=Section and base_class=WeakNode."""
        result = self.graph.schema_yaml("test")
        self.assertIn("parent: Section", result)
        self.assertIn("parent_relation: HAS_PAGE", result)

    def test_character_is_not_weaknode(self) -> None:
        """Character has no parent → base_class=Node."""
        result = self.graph.schema_yaml("test")
        # Character should appear with base_class: Node (not WeakNode)
        self.assertIn("Character:", result)

    def test_document_is_not_weaknode(self) -> None:
        """Document is a root label → base_class=Node."""
        result = self.graph.schema_yaml("test")
        self.assertIn("Document:", result)

    def test_hierarchy_in_valid_yaml(self) -> None:
        """Generated YAML with hierarchies is valid and parseable."""
        if yaml is None:
            self.skipTest("PyYAML not installed")
        result = self.graph.schema_yaml("test")
        data = yaml.safe_load(result)
        labels = data["labels"]
        # Section should have parent
        self.assertIn("parent", labels["Section"])
        self.assertEqual(labels["Section"]["parent"], "Document")
        # Page should have parent
        self.assertIn("parent", labels["Page"])
        self.assertEqual(labels["Page"]["parent"], "Section")
        # Character should not have parent
        self.assertNotIn("parent", labels["Character"])
        # Document should not have parent
        self.assertNotIn("parent", labels["Document"])

    def test_hierarchy_parent_relation(self) -> None:
        """Parent relations are correctly inferred."""
        if yaml is None:
            self.skipTest("PyYAML not installed")
        result = self.graph.schema_yaml("test")
        data = yaml.safe_load(result)
        labels = data["labels"]
        self.assertEqual(labels["Section"]["parent_relation"], "HAS_SECTION")
        self.assertEqual(labels["Page"]["parent_relation"], "HAS_PAGE")

    def test_hierarchy_base_class(self) -> None:
        """Root labels have base_class=Node, children have WeakNode."""
        if yaml is None:
            self.skipTest("PyYAML not installed")
        result = self.graph.schema_yaml("test")
        data = yaml.safe_load(result)
        labels = data["labels"]
        self.assertEqual(labels["Document"]["base_class"], "Node")
        self.assertEqual(labels["Character"]["base_class"], "Node")
        self.assertEqual(labels["Section"]["base_class"], "WeakNode")
        self.assertEqual(labels["Page"]["base_class"], "WeakNode")

    def test_hierarchy_pk_fields(self) -> None:
        """WeakNode primary_key should only include child-specific fields."""
        if yaml is None:
            self.skipTest("PyYAML not installed")
        result = self.graph.schema_yaml("test")
        data = yaml.safe_load(result)
        labels = data["labels"]
        # Section's primary_key should be ['title'], not ['id', 'title']
        # because 'id' comes from Document
        self.assertEqual(labels["Section"]["primary_key"], ["title"])
        # Page's primary_key should be ['number']
        self.assertEqual(labels["Page"]["primary_key"], ["number"])


if __name__ == "__main__":
    unittest.main()
