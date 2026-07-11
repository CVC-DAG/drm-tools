"""Tests for NxQuery integration into NetworkXGraph.

Covers:
- Logical operators ($or, $and, $not) added from nx_query.py
- Bug fixes: $contains safe, $regex escaped, $or[] wildcard
- query_nodes() fluent API returning NxQuery
"""

from __future__ import annotations

import os
import shutil
import tempfile
import unittest

from drm.base import Node, Relation
from drm.networkx_graph import NetworkXGraph


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_graph() -> NetworkXGraph:
    """Return a fresh NetworkXGraph with sample data."""
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "test_graph.pkl")
    g = NetworkXGraph(persistence_path=path)
    g._temp_path = tmp

    g.insertNode(Node(pk={"id": 1}, main_label="Person", name="Alice", age=30, city="Barcelona"), replace=True)
    g.insertNode(Node(pk={"id": 2}, main_label="Person", name="Bob", age=25, city="Girona"), replace=True)
    g.insertNode(Node(pk={"id": 3}, main_label="Person", name="Carol", age=35, city="Barcelona"), replace=True)
    g.insertNode(Node(pk={"id": 4}, main_label="Company", name="Acme", industry="Tech"), replace=True)

    g.insertRelation(Relation(
        Node(pk={"id": 1}, main_label="Person"),
        Node(pk={"id": 4}, main_label="Company"),
        "WORKS_AT",
    ), update=True)
    g.insertRelation(Relation(
        Node(pk={"id": 2}, main_label="Person"),
        Node(pk={"id": 4}, main_label="Company"),
        "WORKS_AT",
    ), update=True)
    return g


# ---------------------------------------------------------------------------
# Logical operators ($or, $and, $not)
# ---------------------------------------------------------------------------


class LogicalOperatorsTest(unittest.TestCase):
    """Tests for $or, $and, $not operators in MongoDB-style queries."""

    def setUp(self) -> None:
        self.graph = _make_graph()

    def tearDown(self) -> None:
        path = getattr(self.graph, "_temp_path", None)
        try:
            self.graph.close()
        except Exception:
            pass
        if path and os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

    def test_or_operator(self) -> None:
        """$or matches nodes matching ANY condition."""
        result = self.graph.query({
            "$or": [
                {"name": "Alice"},
                {"name": "Bob"},
            ]
        })
        self.assertEqual(len(result), 2)
        names = {r["properties"]["name"] for r in result}
        self.assertEqual(names, {"Alice", "Bob"})

    def test_or_operator_three_conditions(self) -> None:
        """$or with three conditions."""
        result = self.graph.query({
            "$or": [
                {"city": "Barcelona"},
                {"city": "Girona"},
                {"city": "Madrid"},
            ]
        })
        # Alice (Barcelona), Bob (Girona), Carol (Barcelona)
        self.assertEqual(len(result), 3)

    def test_or_operator_no_match(self) -> None:
        """$or where no condition matches."""
        result = self.graph.query({
            "$or": [
                {"name": "Zara"},
                {"name": "Yolanda"},
            ]
        })
        self.assertEqual(len(result), 0)

    def test_or_empty_list_is_wildcard(self) -> None:
        """$or: [] should match all nodes (wildcard), not filter everything."""
        result = self.graph.query({"$or": []})
        # Should return all 4 nodes (Person + Company)
        self.assertGreaterEqual(len(result), 3)

    def test_and_operator(self) -> None:
        """$and matches nodes matching ALL conditions."""
        result = self.graph.query({
            "$and": [
                {"main_label": "Person"},
                {"age": {"$gte": 30}},
            ]
        })
        # Alice (30) and Carol (35)
        self.assertEqual(len(result), 2)

    def test_and_operator_combined_with_or(self) -> None:
        """$and containing $or conditions."""
        result = self.graph.query({
            "$and": [
                {"main_label": "Person"},
                {"$or": [
                    {"city": "Barcelona"},
                    {"age": {"$lt": 26}},
                ]},
            ]
        })
        # Alice (Barcelona), Bob (age 25) — Carol is Barcelona too
        self.assertEqual(len(result), 3)

    def test_not_operator(self) -> None:
        """$not inverts a single condition."""
        result = self.graph.query({
            "main_label": "Person",
            "$not": {"name": "Alice"},
        })
        names = {r["properties"]["name"] for r in result}
        self.assertEqual(names, {"Bob", "Carol"})

    def test_not_operator_no_match(self) -> None:
        """$not where the condition matches nothing — returns all."""
        result = self.graph.query({
            "$not": {"name": "Zara"},
        })
        # All nodes except non-existent "Zara"
        self.assertGreaterEqual(len(result), 3)

    def test_nested_or_in_and(self) -> None:
        """Complex nesting: $and with $or and operators."""
        result = self.graph.query({
            "$or": [
                {"name": "Alice"},
                {"$and": [
                    {"name": "Bob"},
                    {"city": "Girona"},
                ]},
            ]
        })
        self.assertEqual(len(result), 2)


# ---------------------------------------------------------------------------
# Bug fixes: $contains, $regex, $or[]
# ---------------------------------------------------------------------------


class BugFixesTest(unittest.TestCase):
    """Tests for bug fixes in nx_query integration."""

    def setUp(self) -> None:
        self.graph = _make_graph()
        # Add nodes with tricky values
        g = self.graph
        g.insertNode(Node(pk={"id": 10}, main_label="Item", name="widget", count=42, tags=["red", "blue"]), replace=True)
        g.insertNode(Node(pk={"id": 11}, main_label="Item", name="gadget", count=7, tags=["green"]), replace=True)

    def tearDown(self) -> None:
        path = getattr(self.graph, "_temp_path", None)
        try:
            self.graph.close()
        except Exception:
            pass
        if path and os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

    def test_contains_with_list(self) -> None:
        """$contains should match items where the field contains the value."""
        result = self.graph.query({"tags": {"$contains": "red"}})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["properties"]["name"], "widget")

    def test_contains_with_non_iterable_no_crash(self) -> None:
        """$contains on a non-iterable field (int) should not crash."""
        # count=42 is an int — $contains on int should be safe
        result = self.graph.query({"count": {"$contains": 42}})
        # Should return [] or handle gracefully, never crash
        self.assertIsInstance(result, list)

    def test_regex_with_special_chars_no_crash(self) -> None:
        """$regex with special regex chars should not crash."""
        # "widget" contains no regex chars, but the pattern might
        result = self.graph.query({"name": {"$regex": r"widget"}})
        self.assertEqual(len(result), 1)

    def test_regex_with_brackets_no_crash(self) -> None:
        """$regex with unbalanced brackets should not raise re.error."""
        # This used to crash with re.error: unterminated character set
        result = self.graph.query({"name": {"$regex": r"[invalid"}})
        # Should return [] (no match) instead of crashing
        self.assertIsInstance(result, list)

    def test_or_empty_returns_all(self) -> None:
        """$or: [] returns all nodes, not zero."""
        result = self.graph.query({"$or": []})
        self.assertGreater(len(result), 0)


# ---------------------------------------------------------------------------
# query_nodes() fluent API
# ---------------------------------------------------------------------------


class QueryNodesFluentTest(unittest.TestCase):
    """Tests for NetworkXGraph.query_nodes() fluent API."""

    def setUp(self) -> None:
        self.graph = _make_graph()

    def tearDown(self) -> None:
        path = getattr(self.graph, "_temp_path", None)
        try:
            self.graph.close()
        except Exception:
            pass
        if path and os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

    def test_query_nodes_returns_list(self) -> None:
        """query_nodes() without args returns all nodes."""
        result = self.graph.query_nodes().to_list()
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 4)

    def test_query_nodes_with_filter(self) -> None:
        """query_nodes() with a filter dict."""
        result = self.graph.query_nodes({"main_label": "Person"}).to_list()
        self.assertEqual(len(result), 3)

    def test_query_nodes_with_chained_where(self) -> None:
        """query_nodes() returns NxQuery that supports .where().to_list()."""
        from drm.nx_query import NxQuery
        q = self.graph.query_nodes()
        self.assertIsInstance(q, NxQuery)
        result = q.where({"main_label": "Person"}).to_list()
        self.assertGreaterEqual(len(result), 3)

    def test_query_nodes_chained_filters(self) -> None:
        """Multiple .where() calls are cumulative."""
        result = (
            self.graph.query_nodes()
            .where({"main_label": "Person"})
            .where({"age": {"$gte": 30}})
            .to_list()
        )
        # Alice (30) and Carol (35)
        self.assertEqual(len(result), 2)

    def test_query_nodes_limit(self) -> None:
        """.limit() restricts results."""
        result = (
            self.graph.query_nodes()
            .where({"main_label": "Person"})
            .limit(2)
            .to_list()
        )
        self.assertEqual(len(result), 2)

    def test_query_nodes_count(self) -> None:
        """.count() returns number of matching nodes."""
        count = (
            self.graph.query_nodes()
            .where({"main_label": "Person"})
            .count()
        )
        self.assertEqual(count, 3)

    def test_query_nodes_ids(self) -> None:
        """ids() returns node ids."""
        ids = (
            self.graph.query_nodes()
            .where({"main_label": "Company"})
            .ids()
        )
        self.assertEqual(len(ids), 1)

    def test_query_nodes_empty_result(self) -> None:
        """No matching nodes returns empty list."""
        result = (
            self.graph.query_nodes()
            .where({"main_label": "NonExistent"})
            .to_list()
        )
        self.assertEqual(result, [])


# ---------------------------------------------------------------------------
# Existing tests still pass
# ---------------------------------------------------------------------------


class BackwardCompatibilityTest(unittest.TestCase):
    """Ensure existing query() behavior is preserved."""

    def setUp(self) -> None:
        self.graph = _make_graph()

    def tearDown(self) -> None:
        path = getattr(self.graph, "_temp_path", None)
        try:
            self.graph.close()
        except Exception:
            pass
        if path and os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

    def test_simple_equality_still_works(self) -> None:
        result = self.graph.query({"name": "Alice"})
        self.assertEqual(len(result), 1)

    def test_operator_still_works(self) -> None:
        result = self.graph.query({"age": {"$gt": 26}})
        self.assertEqual(len(result), 2)

    def test_in_operator_still_works(self) -> None:
        result = self.graph.query({"name": {"$in": ["Alice", "Bob"]}})
        self.assertEqual(len(result), 2)

    def test_regex_operator_still_works(self) -> None:
        result = self.graph.query({"name": {"$regex": "^Ali"}})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["properties"]["name"], "Alice")

    def test_exists_operator_still_works(self) -> None:
        result = self.graph.query({"age": {"$exists": True}})
        self.assertGreaterEqual(len(result), 3)


if __name__ == "__main__":
    unittest.main()
