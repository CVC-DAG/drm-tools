"""Mock graph store backed by NetworkX — no real Neo4j required."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union

import networkx as nx

from .base import Node, Relation, WeakRelation


class MockGraph:
    """In-memory graph store using NetworkX.

    Provides the same public interface as ``Neo4jGraph`` but stores
    nodes and edges in a NetworkX MultiDiGraph so tests can run
    without a real database.
    """

    def __init__(self) -> None:
        self._graph: nx.MultiDiGraph = nx.MultiDiGraph()
        self._node_attrs: Dict[int, Dict[str, Any]] = {}
        self._edge_attrs: Dict[Tuple[int, int, int], Dict[str, Any]] = {}
        self._node_counter: int = 0
        self._version: float = 0.0

    # ------------------------------------------------------------------
    # Public API (mirrors Neo4jGraph)
    # ------------------------------------------------------------------

    def insertNode(
        self,
        node: Node,
        insert_parent: bool = True,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> int:
        """Insert a node into the graph.

        Returns the internal node id assigned by the graph.
        """
        # Handle parent insertion for weak nodes
        if node["is_weak"] and insert_parent and node["parent"] is not None:
            parent = node["parent"]
            parent_id: Optional[int] = self._ensure_node_inserted(parent, update=True, replace=False)
            parent.neo4j_id = parent_id

        node_id = self._ensure_node_inserted(node, update=update, replace=replace)
        node.neo4j_id = node_id

        # If weak, create the parent relation
        if node["is_weak"] and node["parent"] is not None:
            parent_id = node["parent"].neo4j_id
            self._graph.add_edge(parent_id, node_id, key=node["parent_relation"], rel_type=node["parent_relation"])
            self._edge_attrs[(parent_id, node_id, node["parent_relation"])] = {}

        # Note: dependencies are NOT automatically inserted here.
        # In Neo4jGraph, dependencies are handled separately in insertNode
        # before calling _insertNode. The mock focuses on the core graph
        # operations.

        return node_id

    def insertRelation(
        self,
        rel: Relation,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> int:
        """Insert a relation (directed edge) between two nodes.

        Returns the internal edge identifier (u, v, key).
        """
        # Resolve src/dst ids: prefer neo4j_id, fall back to pk lookup
        src_id = self._resolve_node_id(rel["src"])
        dst_id = self._resolve_node_id(rel["dst"])

        if src_id is None or dst_id is None:
            raise RuntimeError(
                f"Cannot resolve node ids: src={src_id}, dst={dst_id}. "
                f"Ensure src and dst nodes have been inserted first."
            )

        edge_key = rel["type"]
        self._graph.add_edge(src_id, dst_id, key=edge_key, rel_type=rel["type"])
        attrs = rel["attributes"] if rel["attributes"] is not None else {}
        self._edge_attrs[(src_id, dst_id, edge_key)] = attrs

        return (src_id, dst_id, edge_key)

    def deleteNode(
        self,
        node: Node,
        propagation: bool = False,
        detach: bool = False,
    ) -> bool:
        """Delete a node from the graph."""
        node_id = node.neo4j_id
        if node_id is None:
            return False

        if propagation:
            # Delete all connected nodes that have _propagate=True
            for neighbor in self._graph.predecessors(node_id):
                for key, data in self._graph[neighbor][node_id].items():
                    if data.get("rel_type") and self._edge_attrs.get((neighbor, node_id, key), {}).get("_propagate"):
                        pred_node = Node(neo4j_id=neighbor)
                        self.deleteNode(pred_node, propagation=propagation, detach=True)

        if detach:
            self._graph.remove_node(node_id)
        else:
            # Check if node has edges before removing
            if self._graph.degree(node_id) == 0:
                self._graph.remove_node(node_id)
            else:
                return False

        return True

    def checkNode(self, node: Node, **kwargs: Any) -> Optional[int]:
        """Check if a node exists in the graph.

        Returns the node id if found, None otherwise.
        """
        # Try by neo4j_id first
        if node.neo4j_id is not None:
            if self._graph.has_node(node.neo4j_id):
                return node.neo4j_id
            return None

        # Search by primary key
        pk = node._primary_key
        if pk is None:
            return None

        for node_id, attrs in self._node_attrs.items():
            # Must match main_label AND all pk fields
            if attrs.get("main_label") == node.main_label and self._attrs_match_pk(attrs, pk):
                return node_id

        return None

    def create(
        self,
        migration: Tuple[List, List],
        update: bool = False,
        replace: bool = False,
    ) -> None:
        """Bulk import nodes and relations."""
        node_info, rel_info = migration
        for node in node_info:
            self.insertNode(node, update=update, replace=replace)
        for rel in rel_info:
            self.insertRelation(rel, update=update, replace=replace)

    def close(self) -> None:
        """Release resources (no-op for in-memory graph)."""
        self._graph.clear()
        self._node_attrs.clear()
        self._edge_attrs.clear()

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get_node(self, node_id: int) -> Optional[Node]:
        """Retrieve a node by its internal id."""
        if self._graph.has_node(node_id):
            attrs = self._node_attrs.get(node_id, {})
            labels = attrs.get("labels", [])
            main_label = attrs.get("main_label", "")
            pk = attrs.get("pk", {})
            return Node(neo4j_id=node_id, pk=pk, main_label=main_label, alternative_labels=labels)
        return None

    def get_nodes(self) -> List[int]:
        """Return all node ids."""
        return list(self._graph.nodes())

    def get_edges(self) -> List[Tuple[int, int, str]]:
        """Return all edges as (src_id, dst_id, rel_type) tuples."""
        result = []
        for u, v, key, data in self._graph.edges(data=True, keys=True):
            result.append((u, v, data.get("rel_type", key)))
        return result

    def get_node_attrs(self, node_id: int) -> Optional[Dict[str, Any]]:
        """Return attributes stored for a node."""
        return self._node_attrs.get(node_id)

    def get_edge_attrs(self, u: int, v: int, key: str) -> Optional[Dict[str, Any]]:
        """Return attributes stored for an edge."""
        return self._edge_attrs.get((u, v, key))

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _resolve_node_id(self, node_data: Union[Node, Dict[str, Any]]) -> Optional[int]:
        """Resolve a node or node dict to its internal graph id."""
        if isinstance(node_data, Node):
            if node_data.neo4j_id is not None and self._graph.has_node(node_data.neo4j_id):
                return node_data.neo4j_id
            return self.checkNode(node_data)

        if isinstance(node_data, dict):
            nid = node_data.get("neo4j_id")
            if nid is not None and self._graph.has_node(nid):
                return nid
            # Try to find by pk
            pk = node_data.get("pk")
            if pk and isinstance(pk, dict):
                main_label = node_data.get("main_label")
                for node_id, attrs in self._node_attrs.items():
                    if attrs.get("main_label") == main_label and self._attrs_match_pk(attrs, pk):
                        return node_id

        return None

    def _attrs_match_pk(self, attrs: Dict[str, Any], pk: Dict[str, Any]) -> bool:
        """Check if node attributes match a primary key dict."""
        for k, v in pk.items():
            attr_val = attrs.get(k)
            if attr_val is None:
                return False
            # Compare as strings to handle int/str mismatches
            if str(attr_val) != str(v):
                return False
        return True

    def _ensure_node_inserted(
        self,
        node: Node,
        update: bool = False,
        replace: bool = False,
    ) -> int:
        """Ensure the node exists, returning its id."""
        existing = self.checkNode(node)
        if existing is not None:
            if replace:
                self._graph.remove_node(existing)
                del self._node_attrs[existing]
                self._node_counter += 1
                node_id = self._node_counter
            elif update:
                # Update attributes in-place
                node_id = existing
                pk, attributes = node.attributes
                props = attributes if pk is None else {**pk, **attributes}
                self._node_attrs[node_id].update(props)
                self._graph.nodes[node_id].update(props)
                node.neo4j_id = node_id
                return node_id
            else:
                return existing
        else:
            self._node_counter += 1
            node_id = self._node_counter

        # Store node attributes
        pk, attributes = node.attributes
        props = attributes if pk is None else {**pk, **attributes}
        self._node_attrs[node_id] = {
            "pk": pk,
            "main_label": node.main_label,
            "labels": node.labels,
            **props,
        }

        self._graph.add_node(node_id, **props)
        return node_id
