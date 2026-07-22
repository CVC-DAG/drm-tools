"""Tests for WeakRelation inference in schema_yaml().

WeakRelations are inferred from WeakNode hierarchies: if label A
is a WeakNode child of label B, then the relationship between them
is a WeakRelation with _propagate=true.
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

from cvcdocdb.base import Node, Relation, WeakNode
from cvcdocdb.networkx_graph import NetworkXGraph


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

    # Page (WeakNode of Section)
    page1 = WeakNode(pk={"number": 1}, main_label="Page",
                     parent=sec1, parent_relation="HAS_PAGE")
    g.insertNode(page1, replace=True)

    # Regular relation (not WeakRelation)
    g.insertNode(Node(pk={"name": "Jon Snow"}, main_label="Character",
                      house="Stark"), replace=True)
    g.insertNode(Node(pk={"name": "Arya"}, main_label="Character",
                      house="Stark"), replace=True)
    g.insertRelation(Relation(
        Node(pk={"name": "Jon Snow"}, main_label="Character"),
        Node(pk={"name": "Arya"}, main_label="Character"),
        "KNOWS",
        strength="strong",
    ), update=True)

    return g


# ---------------------------------------------------------------------------
# WeakRelation inference
# ---------------------------------------------------------------------------


class WeakRelationTest(unittest.TestCase):
    """Tests for WeakRelation inference from WeakNode hierarchies."""

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

    def test_weak_relations_section(self) -> None:
        """HAS_SECTION is a WeakRelation."""
        result = self.graph.schema_yaml("test")
        self.assertIn("HAS_SECTION:", result)
        self.assertIn("base_class: WeakRelation", result)
        self.assertIn("propagate: true", result)

    def test_weak_relations_page(self) -> None:
        """HAS_PAGE is a WeakRelation."""
        result = self.graph.schema_yaml("test")
        self.assertIn("HAS_PAGE:", result)
        self.assertIn("base_class: WeakRelation", result)
        self.assertIn("propagate: true", result)

    def test_regular_relation_not_weak(self) -> None:
        """KNOWS is NOT a WeakRelation."""
        if yaml is None:
            self.skipTest("PyYAML not installed")
        result = self.graph.schema_yaml("test")
        data = yaml.safe_load(result)
        self.assertIn("KNOWS", data["relationships"])
        self.assertNotIn("KNOWS", data.get("weak_relations", {}))

    def test_weak_relations_in_yaml(self) -> None:
        """Generated YAML has weak_relations section."""
        if yaml is None:
            self.skipTest("PyYAML not installed")
        result = self.graph.schema_yaml("test")
        data = yaml.safe_load(result)
        self.assertIn("weak_relations", data)
        wr = data["weak_relations"]
        self.assertIn("HAS_SECTION", wr)
        self.assertIn("HAS_PAGE", wr)
        self.assertEqual(wr["HAS_SECTION"]["base_class"], "WeakRelation")
        self.assertTrue(wr["HAS_SECTION"]["propagate"])
        self.assertEqual(wr["HAS_PAGE"]["base_class"], "WeakRelation")
        self.assertTrue(wr["HAS_PAGE"]["propagate"])

    def test_regular_relations_separate(self) -> None:
        """Regular relations stay in the relationships section."""
        if yaml is None:
            self.skipTest("PyYAML not installed")
        result = self.graph.schema_yaml("test")
        data = yaml.safe_load(result)
        self.assertIn("relationships", data)
        self.assertIn("KNOWS", data["relationships"])
        # KNOWS should NOT be in weak_relations
        self.assertNotIn("KNOWS", data.get("weak_relations", {}))

    def test_weak_relation_class_name(self) -> None:
        """WeakRelation class names are camelCase."""
        if yaml is None:
            self.skipTest("PyYAML not installed")
        result = self.graph.schema_yaml("test")
        data = yaml.safe_load(result)
        wr = data["weak_relations"]
        self.assertEqual(wr["HAS_SECTION"]["class_name"], "HasSection")
        self.assertEqual(wr["HAS_PAGE"]["class_name"], "HasPage")


if __name__ == "__main__":
    unittest.main()
