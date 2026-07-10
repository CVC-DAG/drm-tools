"""NetworkX-backed graph store — in-memory, no real Neo4j required."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple, Union

import networkx as nx

from .base import Node, Relation, WeakRelation
from .graph_store import GraphStore


class NetworkXGraph(GraphStore):
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
        # FK index: node_id → set of (other_id, rel_type, direction)
        # direction: "out" means edge starts at this node, "in" means edge ends here
        self._fk_index: Dict[int, Set[Tuple[int, str, str]]] = {}

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

        return (src_id, dst_id, edge_key)

    def _remove_node_attrs(self, node_id: int) -> None:
        """Remove internal bookkeeping for a node."""
        self._node_attrs.pop(node_id, None)
        self._edge_attrs = {
            k: v for k, v in self._edge_attrs.items()
            if k[0] != node_id and k[1] != node_id
        }

    def _set_null_delete(self, node_id: int) -> None:
        """ON DELETE SET NULL: delete node, remove connected edges, keep neighbors.

        Unlike CASCADE, this does NOT recurse into neighbor nodes.
        Edges are removed (required by the graph model), but neighbor
        nodes remain as standalone entities.
        """
        self._clean_fk_index(node_id)
        self._remove_node_attrs(node_id)

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
        self._node_attrs.pop(node_id, None)

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
            self._node_attrs.pop(node_id, None)
            self._graph.remove_node(node_id)

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

    def close(self) -> None:
        """Release resources and clear the graph.

        Clears all nodes, edges, and internal indexes. Equivalent to
        resetting the graph to its initial empty state.
        """
        self._graph.clear()
        self._node_attrs.clear()
        self._edge_attrs.clear()
        self._fk_index.clear()

    # ------------------------------------------------------------------
    # Query helpers
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

    def get_nodes(self) -> List[int]:
        """Return all node ids in the graph."""
        return list(self._graph.nodes())

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
        for nid, entries in state["fk_index"].items():
            print(f"  [{nid}] -> {entries}")
        print("=======================\n")

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
                pk, attributes = node.attributes
                props = attributes if pk is None else {**pk, **attributes}
                self._node_attrs[node_id].update(props)
                self._graph.nodes[node_id].update(props)
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

        self._graph.add_node(node_id, **props)
        return node_id
