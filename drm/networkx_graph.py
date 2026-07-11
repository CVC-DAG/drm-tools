"""NetworkX-backed graph store — in-memory, no real Neo4j required."""

from __future__ import annotations

import hashlib
import os
import pickle
import tempfile
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
import networkx as nx

try:
    import hnswlib
except ImportError:  # pragma: no cover - guarded at runtime in vector APIs
    hnswlib = None

from .base import Node, Relation, WeakRelation
from .graph_store import GraphStore


class NetworkXGraph(GraphStore):
    """In-memory graph store using NetworkX.

    Provides the same public interface as ``Neo4jGraph`` but stores
    nodes and edges in a NetworkX MultiDiGraph so tests can run
    without a real database.
    """

    def __init__(self, persistence_path: Optional[str] = None) -> None:
        self._graph: nx.MultiDiGraph = nx.MultiDiGraph()
        self._node_attrs: Dict[int, Dict[str, Any]] = {}
        self._edge_attrs: Dict[Tuple[int, int, str], Dict[str, Any]] = {}
        self._node_counter: int = 0
        self._version: float = 0.0
        # FK index: node_id → set of (other_id, rel_type, direction)
        # direction: "out" means edge starts at this node, "in" means edge ends here
        self._fk_index: Dict[int, Set[Tuple[int, str, str]]] = {}
        self._pk_index: Dict[Tuple[str, Tuple[Tuple[str, str], ...]], int] = {}
        self._property_index: Dict[Tuple[str, Any], Set[int]] = {}
        self._vector_indexes: Dict[str, Any] = {}
        self._vector_index_meta: Dict[str, Dict[str, Any]] = {}
        self._persistence_path = persistence_path or self._default_persistence_path()
        self._load_state()
        # Internal tracking: node_id -> pk dict (for get_node_pks)
        self._node_pks: Dict[int, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Public API: CRUD operations
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
            parent_id: int = self._ensure_node_inserted(parent, update=True, replace=False)
            parent.neo4j_id = parent_id

        node_id = self._ensure_node_inserted(node, update=update, replace=replace)
        node.neo4j_id = node_id

        # Track node_id -> pk mapping for get_node_pks()
        if node._primary_key is not None:
            self._node_pks[node_id] = dict(node._primary_key)

        # If weak, create the parent relation
        if node["is_weak"] and node["parent"] is not None:
            parent_id = node["parent"].neo4j_id
            self._graph.add_edge(parent_id, node_id, key=node["parent_relation"], rel_type=node["parent_relation"])
            self._edge_attrs[(parent_id, node_id, node["parent_relation"])] = {}
            # Register parent-child edge in FK index (like Neo4jGraph)
            self._add_to_fk_index(parent_id, node_id, node["parent_relation"])
            # Propagate _propagate flag if set on the node
            if getattr(node, "_propagate", False):
                self._edge_attrs[(parent_id, node_id, node["parent_relation"])]["_propagate"] = True

        # Handle dependencies: create Valor nodes and HAS_* edges
        deps = getattr(node, "_dependencies", None)
        if deps:
            for k in deps.keys():
                v = deps[k]
                id_v = self._ensure_node_inserted(v, update=True, replace=False)
                v.neo4j_id = id_v
                self.insertRelation(Relation(node, v, k.upper()), update=True)

        self._save_state()
        return node_id

    def insertRelation(
        self,
        rel: Relation,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> int:
        """Insert a relation (directed edge) between two nodes.

        Mirrors Neo4jGraph.insertRelation semantics:

        - ``update=True``: MERGE + SET — adds/updates attributes without
          deleting the relation.
        - ``update=False`` + ``replace=True``: deletes the existing
          relation and creates a fresh one.
        - ``update=False`` + ``replace=False``: creates a new relation.
          If one with the same src/dst/type already exists, raises
          ``RuntimeError`` (duplicate key).

        Returns the internal edge identifier (u, v, key).
        """
        # Resolve src/dst ids: prefer neo4j_id, fall back to pk lookup
        src_id = self._resolve_node_id(rel["src"])
        dst_id = self._resolve_node_id(rel["dst"])

        if src_id is None or dst_id is None:
            missing = []
            if src_id is None:
                src_pk = rel["src"].get("pk", "?")
                src_label = rel["src"].get("main_label", "?")
                missing.append(f"src(pk={src_pk}, label={src_label})")
            if dst_id is None:
                dst_pk = rel["dst"].get("pk", "?")
                dst_label = rel["dst"].get("main_label", "?")
                missing.append(f"dst(pk={dst_pk}, label={dst_label})")
            raise RuntimeError(
                f"FK violation: node(s) not found: {', '.join(missing)}. "
                f"Insert them before creating the relation."
            )

        edge_key = rel["type"]
        exists = self._graph.has_edge(src_id, dst_id, key=edge_key)

        if exists:
            if replace:
                # Delete existing relation and create fresh
                self._graph.remove_edge(src_id, dst_id, key=edge_key)
                if (src_id, dst_id, edge_key) in self._edge_attrs:
                    del self._edge_attrs[(src_id, dst_id, edge_key)]
                self._remove_from_fk_index(src_id, dst_id, edge_key)
            elif update:
                # MERGE + SET: update attributes of existing relation
                attrs = rel["attributes"] if rel["attributes"] is not None else {}
                self._edge_attrs[(src_id, dst_id, edge_key)].update(attrs)
                self._save_state()
                return (src_id, dst_id, edge_key)
            else:
                # Duplicate key — same as Neo4j ConstraintError
                raise RuntimeError(
                    f"Duplicate relation: ({src_id})-[{edge_key}]->({dst_id}) "
                    f"already exists. Use replace=True to overwrite or "
                    f"update=True to merge attributes."
                )

        # Create new relation
        self._graph.add_edge(src_id, dst_id, key=edge_key, rel_type=rel["type"])
        attrs = rel["attributes"] if rel["attributes"] is not None else {}
        self._edge_attrs[(src_id, dst_id, edge_key)] = attrs
        self._add_to_fk_index(src_id, dst_id, edge_key)

        self._save_state()
        return (src_id, dst_id, edge_key)

    def deleteNode(
        self,
        node: Node,
        propagation: bool = False,
        detach: bool = False,
        on_delete: str = "cascade",
    ) -> bool:
        """Delete a node from the graph.

        ``on_delete`` controls FK behavior:

        - ``"cascade"`` (default): ON DELETE CASCADE — delete connected edges
        - ``"restrict"``: ON DELETE RESTRICT — refuse if edges exist
        - ``"set_null"``: ON DELETE SET NULL — delete node, keep neighbors
        """
        node_id = node.neo4j_id
        if node_id is None:
            # Fall back to PK lookup
            node_id = self.checkNode(node)
        if node_id is None:
            return False

        if propagation:
            # Delete all connected nodes that have _propagate=True
            # Neo4j: MATCH (n)-[r]->(b) WHERE r._propagate=TRUE RETURN b
            # Also check if the parent node itself has propagate enabled
            parent_propagate = getattr(node, "_propagate", False)
            # Iterate over a copy since deleteNode mutates the graph
            neighbors = list(self._graph.successors(node_id))
            for neighbor in neighbors:
                edges_data = list(self._graph[node_id][neighbor].items())
                for key, data in edges_data:
                    edge_has_propagate = self._edge_attrs.get((node_id, neighbor, key), {}).get("_propagate")
                    if edge_has_propagate or parent_propagate:
                        child_node = Node(neo4j_id=neighbor)
                        self.deleteNode(child_node, propagation=propagation, detach=True)
                        # Stop iterating if node was deleted
                        break

        if on_delete == "set_null":
            # ON DELETE SET NULL: delete node, remove edges, keep neighbors
            self._set_null_delete(node_id)
            if self._graph.has_node(node_id):
                self._graph.remove_node(node_id)
            self._save_state()
            return True

        if detach:
            # ON DELETE CASCADE: recursively delete connected edges and orphans
            self._cascade_delete(node_id)
            # Remove node from graph if it still exists
            if self._graph.has_node(node_id):
                self._graph.remove_node(node_id)
        else:
            # ON DELETE RESTRICT: refuse to delete if edges exist
            if self._graph.degree(node_id) > 0:
                raise RuntimeError(
                    f"ON DELETE RESTRICT: node {node_id} has edges and "
                    f"detach=False. Use detach=True or remove edges first."
                )
            self._clean_fk_index(node_id)
            old_attrs = self._node_attrs.pop(node_id, None)
            if old_attrs is not None:
                self._deindex_node(node_id, old_attrs)
            self._graph.remove_node(node_id)

        self._save_state()
        return True

    def checkNode(self, node: Node, **kwargs: Any) -> Optional[int]:
        """Check if a node exists in the graph.

        Looks up the node by its ``neo4j_id`` if set, otherwise searches
        by ``main_label`` and primary key.

        Args:
            node: The node to look up.

        Returns:
            The internal node id if found, None otherwise.
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

        idx_key = self._pk_index_key(node.main_label, pk)
        node_id = self._pk_index.get(idx_key)
        if node_id is not None and self._graph.has_node(node_id):
            return node_id

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
        """Bulk import nodes and relations.

        Iterates over the node and relation lists, inserting each with
        the given ``update`` and ``replace`` flags.

        Args:
            migration: A tuple ``(node_list, relation_list)``.
            update: Passed to ``insertNode`` / ``insertRelation``.
            replace: Passed to ``insertNode`` / ``insertRelation``.
        """
        node_info, rel_info = migration
        for node in node_info:
            self.insertNode(node, update=update, replace=replace)
        for rel in rel_info:
            self.insertRelation(rel, update=update, replace=replace)

    # ------------------------------------------------------------------
    # Public API: query operations
    # ------------------------------------------------------------------

    def get_node(self, node_id: int) -> Optional[Node]:
        """Retrieve a node by its internal id.

        Args:
            node_id: The internal node id.

        Returns:
            A ``Node`` instance with the stored attributes, or None
            if no node with that id exists.
        """
        if self._graph.has_node(node_id):
            attrs = self._node_attrs.get(node_id, {})
            labels = attrs.get("labels", [])
            main_label = attrs.get("main_label", "")
            pk = attrs.get("pk", {})
            return Node(neo4j_id=node_id, pk=pk, main_label=main_label, alternative_labels=labels)
        return None

    def get_node_ids(self) -> List[int]:
        """Return all internal node ids in the graph."""
        return list(self._graph.nodes())

    def get_nodes(self) -> List[int]:
        """Alias for :meth:`get_node_ids` for backward compatibility."""
        return self.get_node_ids()

    def get_node_pks(self) -> List[Dict[str, Any]]:
        """Return all primary keys of nodes in the graph."""
        result = []
        for nid, pk in self._node_pks.items():
            if nid in self._graph.nodes:
                node = self._graph.nodes[nid]
                label = node.get("main_label", "")
                result.append({"main_label": label, "pk": pk})
        return result

    def get_edges(self) -> List[Tuple[int, int, str]]:
        """Return all edges as ``(src_id, dst_id, rel_type)`` tuples."""
        result = []
        for u, v, key, data in self._graph.edges(data=True, keys=True):
            result.append((u, v, data.get("rel_type", key)))
        return result

    def get_node_attrs(self, node_id: int) -> Optional[Dict[str, Any]]:
        """Return attributes stored for a node.

        Args:
            node_id: The internal node id.

        Returns:
            A dict of node attributes, or None if the node does not exist.
        """
        return self._node_attrs.get(node_id)

    def get_edge_attrs(self, u: int, v: int, key: str) -> Optional[Dict[str, Any]]:
        """Return attributes stored for an edge.

        Args:
            u: Source node id.
            v: Destination node id.
            key: Edge type / key.

        Returns:
            A dict of edge attributes, or None if the edge does not exist.
        """
        return self._edge_attrs.get((u, v, key))

    def find_nodes_by_property(self, prop_name: str, value: Any) -> List[int]:
        """Return node ids indexed by an exact property value match."""
        idx_key = (prop_name, self._normalize_index_value(value))
        return sorted(self._property_index.get(idx_key, set()))

    def find_nodes(self, filters: Dict[str, Any], match: str = "all") -> List[int]:
        """Find node ids by indexed property filters.

        Args:
            filters: Mapping of property name -> exact value.
            match: ``"all"`` (intersection) or ``"any"`` (union).
        """
        if not filters:
            return self.get_nodes()
        if match not in ("all", "any"):
            raise ValueError("match must be 'all' or 'any'")

        buckets: List[Set[int]] = []
        for prop_name, value in filters.items():
            idx_key = (prop_name, self._normalize_index_value(value))
            buckets.append(set(self._property_index.get(idx_key, set())))

        if not buckets:
            return []
        if match == "all":
            result = set.intersection(*buckets)
        else:
            result = set.union(*buckets)
        return sorted(result)

    def debug(self) -> Dict[str, Any]:
        """Return a human-readable snapshot of the graph state.

        Returns a dict with keys:
        - ``nodes``: list of (id, label, pk)
        - ``edges``: list of (src_id, dst_id, rel_type, attrs)
        - ``fk_index``: dict mapping node_id -> list of (other_id, rel_type, direction)
        """
        return {
            "nodes": [
                (nid, attrs.get("main_label"), attrs.get("pk"))
                for nid, attrs in self._node_attrs.items()
            ],
            "edges": [
                (u, v, data.get("rel_type", key), self._edge_attrs.get((u, v, key), {}))
                for u, v, key, data in self._graph.edges(data=True, keys=True)
            ],
            "fk_index": {
                k: list(v) for k, v in self._fk_index.items()
            },
        }

    def print_debug(self) -> None:
        """Print a formatted snapshot of the graph state to stdout."""
        state = self.debug()
        print("\n=== NetworkXGraph State ===")
        print(f"Nodes ({len(state['nodes'])}):")
        for nid, label, pk in state["nodes"]:
            print(f"  [{nid}] {label} pk={pk}")
        print(f"Edges ({len(state['edges'])}):")
        for u, v, rtype, attrs in state["edges"]:
            print(f"  [{u}] --[{rtype}]--> [{v}] attrs={attrs}")
        print(f"FK Index ({len(state['fk_index'])} entries):")
        for nid, entries in state['fk_index'].items():
            print(f"  [{nid}] -> {entries}")
        print("=======================\n")

    # ------------------------------------------------------------------
    # Public API: lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release resources and clear the graph.

        Persists the current graph state and clears in-memory data.
        """
        self._save_state()
        self._graph.clear()
        self._node_attrs.clear()
        self._edge_attrs.clear()
        self._fk_index.clear()
        self._pk_index.clear()
        self._property_index.clear()
        self._vector_indexes.clear()
        self._vector_index_meta.clear()

    def enable_vector_index(
        self,
        property_name: str,
        dimensions: int,
        space: str = "cosine",
        ef_construction: int = 200,
        m: int = 16,
    ) -> None:
        """Enable ANN vector indexing for a given node property.

        The property values must be 1D vectors with exactly ``dimensions`` items.
        """
        if hnswlib is None:
            raise RuntimeError("hnswlib is required for vector indexing")
        if dimensions <= 0:
            raise ValueError("dimensions must be > 0")
        if space not in ("cosine", "l2", "ip"):
            raise ValueError("space must be one of: cosine, l2, ip")

        current_meta = self._vector_index_meta.get(property_name)
        if current_meta is not None:
            if current_meta["dimensions"] != dimensions or current_meta["space"] != space:
                raise ValueError(
                    f"vector index for '{property_name}' already exists with "
                    f"space={current_meta['space']} dim={current_meta['dimensions']}"
                )
            return

        self._create_empty_vector_index(
            property_name=property_name,
            dimensions=dimensions,
            space=space,
            ef_construction=ef_construction,
            m=m,
            max_elements=max(1024, len(self._node_attrs) + 128),
        )
        self._rebuild_vector_index(property_name)
        self._save_state()

    def query_vector_index(
        self,
        property_name: str,
        vector: Union[List[float], Tuple[float, ...], np.ndarray],
        top_k: int = 10,
    ) -> List[Tuple[int, float]]:
        """Query nearest neighbors by vector similarity for one indexed property."""
        if top_k <= 0:
            return []
        if property_name not in self._vector_indexes:
            raise ValueError(f"vector index for property '{property_name}' is not enabled")

        meta = self._vector_index_meta[property_name]
        label_to_node = meta["label_to_node"]
        if not label_to_node:
            return []

        query_vec = self._coerce_vector(vector, meta["dimensions"])
        query_k = min(top_k, len(label_to_node))
        labels, distances = self._vector_indexes[property_name].knn_query(query_vec.reshape(1, -1), k=query_k)

        results: List[Tuple[int, float]] = []
        for label, dist in zip(labels[0], distances[0]):
            node_id = label_to_node.get(int(label))
            if node_id is not None:
                results.append((node_id, float(dist)))
        return results

    # ------------------------------------------------------------------
    # Protected helpers: node operations
    # ------------------------------------------------------------------

    def _ensure_node_inserted(
        self,
        node: Node,
        update: bool = False,
        replace: bool = False,
    ) -> int:
        """Ensure the node exists, returning its id.

        Mirrors Neo4jGraph._insertNode semantics:

        - ``update=True``: MERGE + SET — adds/updates attributes without
          deleting the node.  The node keeps its existing id.
        - ``update=False`` + ``replace=True``: deletes the existing node
          (detach) and creates a fresh one with a new id.
        - ``update=False`` + ``replace=False``: tries to CREATE a new
          node.  If a node with the same PK already exists this is a
          duplicate-key error (raises ``RuntimeError``).
        """
        existing = self.checkNode(node)

        if existing is not None:
            # Node already exists
            if replace:
                # ON UPDATE CASCADE: in Neo4j, edges reference nodes
                # by internal ID which never changes.  replace=True
                # deletes the node (with detach, cascading edges) and
                # creates a fresh one — the caller must recreate
                # relations if needed.
                self.deleteNode(node, detach=True, propagation=True)
                self._node_counter += 1
                node_id = self._node_counter
            elif update:
                # ON UPDATE CASCADE: PK changes are safe — the FK index is
                # keyed by internal node IDs which never change.  The MERGE
                # + SET in _ensure_node_inserted already updates the PK in
                # _node_attrs, so all relations continue to resolve correctly.
                pass
                # MERGE + SET: merge attributes into existing node
                node_id = existing
                old_attrs = self._node_attrs.get(node_id, {}).copy()
                pk, attributes = node.attributes
                props = attributes if pk is None else {**pk, **attributes}
                self._node_attrs[node_id].update(props)
                self._graph.nodes[node_id].update(props)
                self._deindex_node(node_id, old_attrs)
                self._index_node(node_id, self._node_attrs[node_id])
                self._sync_vector_indexes_for_node(node_id, self._node_attrs[node_id])
                node.neo4j_id = node_id
                return node_id
            else:
                # Duplicate key — same as Neo4j ConstraintError
                raise RuntimeError(
                    f"Duplicate key: node with pk={node._primary_key} "
                    f"and main_label={node.main_label} already exists (id={existing}). "
                    f"Use replace=True to overwrite or update=True to merge attributes."
                )
        else:
            # Node does not exist — create fresh
            self._node_counter += 1
            node_id = self._node_counter

        # Si el node tenia pk=None explícit, assignem l'ID generat com a PK
        if node._primary_key is None:
            node._primary_key = {"id": node_id}

        # Store node attributes
        pk, attributes = node.attributes
        props = attributes if pk is None else {**pk, **attributes}
        self._node_attrs[node_id] = {
            "pk": pk,
            "main_label": node.main_label,
            "labels": node.labels,
            **props,
        }
        self._index_node(node_id, self._node_attrs[node_id])
        self._sync_vector_indexes_for_node(node_id, self._node_attrs[node_id])

        self._graph.add_node(node_id, **props)
        return node_id

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
                idx_key = self._pk_index_key(main_label, pk)
                idx_id = self._pk_index.get(idx_key)
                if idx_id is not None and self._graph.has_node(idx_id):
                    return idx_id
                for node_id, attrs in self._node_attrs.items():
                    if attrs.get("main_label") == main_label and self._attrs_match_pk(attrs, pk):
                        return node_id

        return None

    # ------------------------------------------------------------------
    # Protected helpers: FK index operations
    # ------------------------------------------------------------------

    def _add_to_fk_index(self, src_id: int, dst_id: int, edge_key: str) -> None:
        """Record a new edge in the FK index for both endpoints."""
        self._fk_index.setdefault(src_id, set()).add((dst_id, edge_key, "out"))
        self._fk_index.setdefault(dst_id, set()).add((src_id, edge_key, "in"))

    def _remove_from_fk_index(self, src_id: int, dst_id: int, edge_key: str) -> None:
        """Remove an edge from the FK index."""
        if src_id in self._fk_index:
            self._fk_index[src_id].discard((dst_id, edge_key, "out"))
            if not self._fk_index[src_id]:
                del self._fk_index[src_id]
        if dst_id in self._fk_index:
            self._fk_index[dst_id].discard((src_id, edge_key, "in"))
            if not self._fk_index[dst_id]:
                del self._fk_index[dst_id]

    def _clean_fk_index(self, node_id: int) -> None:
        """Remove all FK index entries for a node being deleted."""
        if node_id in self._fk_index:
            for other_id, edge_key, direction in self._fk_index[node_id]:
                if other_id in self._fk_index:
                    if direction == "out":
                        self._fk_index[other_id].discard((node_id, edge_key, "in"))
                    else:
                        self._fk_index[other_id].discard((node_id, edge_key, "out"))
                    if not self._fk_index[other_id]:
                        del self._fk_index[other_id]
            del self._fk_index[node_id]

    def _cascade_delete(self, node_id: int) -> None:
        """ON DELETE CASCADE: delete node and all connected edges.

        Uses the FK index to find all edges connected to the node (both
        incoming and outgoing) and removes them.  Neighbor nodes are left
        as standalone entities.  Mirrors Neo4jGraph._cascade_delete.
        """
        entries = self._fk_index.get(node_id, set()).copy()
        for neighbor_id, rel_type, direction in entries:
            # Delete the edge in the correct direction
            if direction == "out":
                # Edge: node_id → neighbor_id
                if self._graph.has_edge(node_id, neighbor_id, key=rel_type):
                    self._graph.remove_edge(node_id, neighbor_id, key=rel_type)
                    self._edge_attrs.pop((node_id, neighbor_id, rel_type), None)
            else:
                # Edge: neighbor_id → node_id
                if self._graph.has_edge(neighbor_id, node_id, key=rel_type):
                    self._graph.remove_edge(neighbor_id, node_id, key=rel_type)
                    self._edge_attrs.pop((neighbor_id, node_id, rel_type), None)

            # Clean FK index for neighbor
            if neighbor_id in self._fk_index:
                self._fk_index[neighbor_id] = {
                    e for e in self._fk_index[neighbor_id]
                    if e != (node_id, rel_type, "in" if direction == "out" else "out")
                }
                if not self._fk_index[neighbor_id]:
                    del self._fk_index[neighbor_id]
        self._fk_index.pop(node_id, None)
        old_attrs = self._node_attrs.pop(node_id, None)
        if old_attrs is not None:
            self._deindex_node(node_id, old_attrs)

    def _set_null_delete(self, node_id: int) -> None:
        """ON DELETE SET NULL: delete node, remove connected edges, keep neighbors.

        Unlike CASCADE, this does NOT recurse into neighbor nodes.
        Edges are removed (required by the graph model), but neighbor
        nodes remain as standalone entities.
        """
        self._clean_fk_index(node_id)
        self._remove_node_attrs(node_id)

    def _remove_node_attrs(self, node_id: int) -> None:
        """Remove internal bookkeeping for a node."""
        old_attrs = self._node_attrs.pop(node_id, None)
        if old_attrs is not None:
            self._deindex_node(node_id, old_attrs)
        self._edge_attrs = {
            k: v for k, v in self._edge_attrs.items()
            if k[0] != node_id and k[1] != node_id
        }

    def _reconnect_edges_for_node(self, old_id: int, new_id: int) -> None:
        """ON UPDATE CASCADE for relations: rewire edges from old_id to new_id.

        Edges where old_id is src or dst are redirected to new_id.
        Edges where old_id is in the FK index are also updated.
        """
        # Reconnect edges in the graph where old_id is src
        for neighbor, key, data in list(self._graph.out_edges(old_id, keys=True, data=True)):
            self._graph.remove_edge(old_id, neighbor, key=key)
            self._graph.add_edge(new_id, neighbor, key=key, rel_type=data.get("rel_type", key))
            # Move edge attrs
            attrs = self._edge_attrs.pop((old_id, neighbor, key), {})
            if attrs:
                self._edge_attrs[(new_id, neighbor, key)] = attrs

        # Reconnect edges in the graph where old_id is dst
        for pred, neighbor, key, data in list(self._graph.in_edges(old_id, keys=True, data=True)):
            self._graph.remove_edge(pred, old_id, key=key)
            self._graph.add_edge(pred, new_id, key=key, rel_type=data.get("rel_type", key))
            attrs = self._edge_attrs.pop((pred, old_id, key), {})
            if attrs:
                self._edge_attrs[(pred, new_id, key)] = attrs

        # Update FK index: redirect all entries pointing to old_id
        for other_id in list(self._fk_index):
            self._fk_index[other_id] = {
                (new_id if oid == old_id else oid, rt, d)
                for oid, rt, d in self._fk_index[other_id]
            }
        # Move old_id entries to new_id in FK index
        if old_id in self._fk_index:
            self._fk_index[new_id] = self._fk_index.pop(old_id)

    # ------------------------------------------------------------------
    # Protected helpers: persistence
    # ------------------------------------------------------------------

    def _default_persistence_path(self) -> str:
        """Build a deterministic persistence path for the current workspace."""
        workspace = os.path.abspath(os.getcwd())
        workspace_hash = hashlib.sha1(workspace.encode("utf-8")).hexdigest()[:12]
        filename = f"drm_networkx_graph_{workspace_hash}.pkl"
        return os.path.join(tempfile.gettempdir(), filename)

    def _save_state(self) -> None:
        """Persist the full graph store state atomically."""
        for prop_name, vector_index in self._vector_indexes.items():
            vector_index.save_index(self._vector_index_file(prop_name))

        state = {
            "graph": self._graph,
            "node_attrs": self._node_attrs,
            "edge_attrs": self._edge_attrs,
            "node_counter": self._node_counter,
            "version": self._version,
            "fk_index": self._fk_index,
            "pk_index": self._pk_index,
            "property_index": self._property_index,
            "vector_index_meta": self._vector_index_meta,
        }
        parent_dir = os.path.dirname(self._persistence_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        tmp_path = f"{self._persistence_path}.tmp"
        with open(tmp_path, "wb") as fh:
            pickle.dump(state, fh, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp_path, self._persistence_path)

    def _load_state(self) -> None:
        """Load graph store state from disk if present."""
        if not os.path.exists(self._persistence_path):
            return
        with open(self._persistence_path, "rb") as fh:
            state = pickle.load(fh)
        self._graph = state.get("graph", nx.MultiDiGraph())
        self._node_attrs = state.get("node_attrs", {})
        self._edge_attrs = state.get("edge_attrs", {})
        self._node_counter = state.get("node_counter", 0)
        self._version = state.get("version", 0.0)
        self._fk_index = state.get("fk_index", {})
        self._pk_index = state.get("pk_index", {})
        self._property_index = state.get("property_index", {})
        self._vector_index_meta = state.get("vector_index_meta", {})
        # Backward compatibility with older persistence files without indexes.
        if not self._pk_index and self._node_attrs:
            self._rebuild_indexes()

        self._vector_indexes = {}
        if self._vector_index_meta:
            if hnswlib is None:
                raise RuntimeError("hnswlib is required to load persisted vector indexes")
            for prop_name, meta in self._vector_index_meta.items():
                idx = hnswlib.Index(space=meta["space"], dim=meta["dimensions"])
                vector_path = self._vector_index_file(prop_name)
                if os.path.exists(vector_path):
                    idx.load_index(vector_path, max_elements=meta.get("max_elements", 0))
                    idx.set_ef(max(50, meta.get("ef_construction", 200)))
                    self._vector_indexes[prop_name] = idx
                else:
                    self._create_empty_vector_index(
                        property_name=prop_name,
                        dimensions=meta["dimensions"],
                        space=meta["space"],
                        ef_construction=meta.get("ef_construction", 200),
                        m=meta.get("m", 16),
                        max_elements=max(1024, len(self._node_attrs) + 128),
                    )
                    self._rebuild_vector_index(prop_name)

    # ------------------------------------------------------------------
    # Protected helpers: indexing
    # ------------------------------------------------------------------

    def _index_node(self, node_id: int, attrs: Dict[str, Any]) -> None:
        """Index a node by PK and by scalar properties."""
        pk = attrs.get("pk")
        pk_key = self._pk_index_key(str(attrs.get("main_label", "")), pk if isinstance(pk, dict) else None)
        if pk_key is not None:
            existing = self._pk_index.get(pk_key)
            if existing is not None and existing != node_id:
                raise RuntimeError(
                    f"Duplicate PK: node with pk={pk} "
                    f"and main_label={attrs.get('main_label')} already exists (id={existing})."
                )
            self._pk_index[pk_key] = node_id

        for prop_name, prop_value in attrs.items():
            if prop_name == "pk":
                continue
            idx_key = (prop_name, self._normalize_index_value(prop_value))
            self._property_index.setdefault(idx_key, set()).add(node_id)

    def _deindex_node(self, node_id: int, attrs: Dict[str, Any]) -> None:
        """Remove a node from PK and property indexes."""
        pk = attrs.get("pk")
        pk_key = self._pk_index_key(str(attrs.get("main_label", "")), pk if isinstance(pk, dict) else None)
        if pk_key is not None and self._pk_index.get(pk_key) == node_id:
            del self._pk_index[pk_key]

        for prop_name, prop_value in attrs.items():
            if prop_name == "pk":
                continue
            idx_key = (prop_name, self._normalize_index_value(prop_value))
            node_set = self._property_index.get(idx_key)
            if node_set is None:
                continue
            node_set.discard(node_id)
            if not node_set:
                del self._property_index[idx_key]

        self._remove_node_from_vector_indexes(node_id)

    def _rebuild_indexes(self) -> None:
        """Rebuild all secondary indexes from node attributes."""
        self._pk_index.clear()
        self._property_index.clear()
        for node_id, attrs in self._node_attrs.items():
            self._index_node(node_id, attrs)

    def _normalize_index_value(self, value: Any) -> Any:
        """Convert arbitrary values to a deterministic hashable representation."""
        if isinstance(value, dict):
            return tuple(sorted((str(k), self._normalize_index_value(v)) for k, v in value.items()))
        if isinstance(value, (list, tuple)):
            return tuple(self._normalize_index_value(v) for v in value)
        if isinstance(value, set):
            normalized = [self._normalize_index_value(v) for v in value]
            return tuple(sorted(normalized, key=repr))
        return value

    def _pk_index_key(self, main_label: str, pk: Optional[Dict[str, Any]]) -> Optional[Tuple[str, Tuple[Tuple[str, str], ...]]]:
        """Build the unique PK index key for a node."""
        if pk is None:
            return None
        items = tuple(sorted((str(k), str(v)) for k, v in pk.items()))
        return (str(main_label), items)

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

    # ------------------------------------------------------------------
    # Protected helpers: vector index operations
    # ------------------------------------------------------------------

    def _vector_index_file(self, property_name: str) -> str:
        """Return the on-disk file path for one vector index."""
        digest = hashlib.sha1(property_name.encode("utf-8")).hexdigest()[:12]
        return f"{self._persistence_path}.vectors.{digest}.bin"

    def _coerce_vector(
        self,
        value: Union[List[float], Tuple[float, ...], np.ndarray, Any],
        dimensions: int,
    ) -> np.ndarray:
        """Validate and convert a value into a float32 dense vector."""
        vec = np.asarray(value, dtype=np.float32)
        if vec.ndim != 1 or vec.shape[0] != dimensions:
            raise ValueError(f"expected 1D vector of length {dimensions}, got shape {vec.shape}")
        if not np.all(np.isfinite(vec)):
            raise ValueError("vector contains non-finite values")
        return vec

    def _create_empty_vector_index(
        self,
        property_name: str,
        dimensions: int,
        space: str,
        ef_construction: int,
        m: int,
        max_elements: int,
    ) -> None:
        """Create and register an empty hnswlib index for one property."""
        if hnswlib is None:
            raise RuntimeError("hnswlib is required for vector indexing")

        idx = hnswlib.Index(space=space, dim=dimensions)
        idx.init_index(
            max_elements=max_elements,
            ef_construction=ef_construction,
            M=m,
            allow_replace_deleted=True,
        )
        idx.set_ef(max(50, ef_construction))

        self._vector_indexes[property_name] = idx
        self._vector_index_meta[property_name] = {
            "space": space,
            "dimensions": dimensions,
            "ef_construction": ef_construction,
            "m": m,
            "max_elements": max_elements,
            "next_label": 0,
            "label_to_node": {},
            "node_to_label": {},
        }

    def _ensure_vector_capacity(self, property_name: str, required: int) -> None:
        """Resize an hnswlib index if we exceed allocated elements."""
        meta = self._vector_index_meta[property_name]
        current_max = int(meta.get("max_elements", 0))
        if required <= current_max:
            return
        new_max = max(required, max(1024, current_max * 2))
        self._vector_indexes[property_name].resize_index(new_max)
        meta["max_elements"] = new_max

    def _sync_vector_index_for_node(self, property_name: str, node_id: int, attrs: Dict[str, Any]) -> None:
        """Insert/update one node vector inside one vector index."""
        if property_name not in self._vector_indexes:
            return

        meta = self._vector_index_meta[property_name]
        node_to_label = meta["node_to_label"]
        label_to_node = meta["label_to_node"]

        if property_name not in attrs:
            if node_id in node_to_label:
                self._rebuild_vector_index(property_name)
            return

        vector = self._coerce_vector(attrs[property_name], meta["dimensions"])

        label = node_to_label.get(node_id)
        if label is None:
            label = int(meta["next_label"])
            meta["next_label"] = label + 1
            self._ensure_vector_capacity(property_name, len(label_to_node) + 1)
            self._vector_indexes[property_name].add_items(vector.reshape(1, -1), np.array([label], dtype=np.int64))
            node_to_label[node_id] = label
            label_to_node[label] = node_id
            return

        self._vector_indexes[property_name].add_items(vector.reshape(1, -1), np.array([label], dtype=np.int64))

    def _sync_vector_indexes_for_node(self, node_id: int, attrs: Dict[str, Any]) -> None:
        """Insert/update one node across all enabled vector indexes."""
        for property_name in list(self._vector_indexes.keys()):
            self._sync_vector_index_for_node(property_name, node_id, attrs)

    def _remove_node_from_vector_indexes(self, node_id: int) -> None:
        """Remove one node from vector indexes by rebuilding affected indexes."""
        affected = [
            prop_name
            for prop_name, meta in self._vector_index_meta.items()
            if node_id in meta.get("node_to_label", {})
        ]
        for prop_name in affected:
            self._rebuild_vector_index(prop_name)

    def _rebuild_vector_index(self, property_name: str) -> None:
        """Rebuild one vector index from current node attributes."""
        if property_name not in self._vector_index_meta:
            return

        meta = self._vector_index_meta[property_name]
        self._create_empty_vector_index(
            property_name=property_name,
            dimensions=int(meta["dimensions"]),
            space=str(meta["space"]),
            ef_construction=int(meta.get("ef_construction", 200)),
            m=int(meta.get("m", 16)),
            max_elements=max(1024, len(self._node_attrs) + 128),
        )
        for node_id, attrs in self._node_attrs.items():
            self._sync_vector_index_for_node(property_name, node_id, attrs)
