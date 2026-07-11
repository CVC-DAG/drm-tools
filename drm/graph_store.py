"""Abstract graph store interface for the DRM model.

Both ``Neo4jGraph`` and ``NetworkXGraph`` implement this ABC so that
code in ``entities.py`` and elsewhere can accept any graph store
without knowing the backing technology.

Usage::

    from drm.graph_store import GraphStore
    from drm.networkx_graph import NetworkXGraph

    def process(store: GraphStore) -> None:
        node = Node(pk={"id": 1}, main_label="Test")
        store.insertNode(node)
        store.close()

    process(NetworkXGraph())
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from .base import Node, Relation


class GraphStore(ABC):
    """Abstract interface for graph-backed stores (Neo4j, NetworkX, etc.).

    Every concrete implementation must support the same core operations:
    insert, update, replace, delete nodes and relations, bulk import,
    and existence checks.

    Subclasses must implement all abstract methods.
    """

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------

    @abstractmethod
    def insertNode(
        self,
        node: Node,
        insert_parent: bool = True,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> Union[int, str]:
        """Insert a node into the graph store.

        Args:
            node: The node to insert.
            insert_parent: If the node is a WeakNode, insert its parent
                first. Defaults to True.
            update: If True, MERGE the node and update attributes without
                deleting it. Defaults to False.
            replace: If True and the node already exists, delete it
                (with detach) and create a fresh one. Defaults to False.
            **kwargs: Additional implementation-specific parameters.

        Returns:
            The internal node identifier assigned by the store.
        """

    @abstractmethod
    def insertRelation(
        self,
        rel: Relation,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> Union[int, Tuple[int, int, str]]:
        """Insert a directed relation (edge) between two nodes.

        Args:
            rel: The relation to insert.
            update: If True, MERGE the relation and update attributes.
            replace: If True and the relation already exists, delete it
                and create a fresh one.
            **kwargs: Additional implementation-specific parameters.

        Returns:
            The internal relation identifier.
        """

    @abstractmethod
    def deleteNode(
        self,
        node: Node,
        propagation: bool = False,
        detach: bool = False,
        on_delete: str = "cascade",
    ) -> bool:
        """Delete a node from the graph store.

        Args:
            node: The node to delete.
            propagation: If True, recursively delete child nodes linked
                via edges with ``_propagate=TRUE``.
            detach: If True, delete the node and all connected edges.
            on_delete: Deletion strategy — ``"cascade"``, ``"restrict"``,
                or ``"set_null"``. Defaults to ``"cascade"``.

        Returns:
            True if the node was deleted, False otherwise.
        """

    @abstractmethod
    def checkNode(self, node: Node, **kwargs: Any) -> Optional[int]:
        """Check if a node exists in the graph store.

        Args:
            node: The node to look up.
            **kwargs: Additional implementation-specific parameters.

        Returns:
            The internal node id if found, None otherwise.
        """

    @abstractmethod
    def create(
        self,
        migration: Tuple[List, List],
        update: bool = False,
        replace: bool = False,
    ) -> None:
        """Bulk import nodes and relations.

        Args:
            migration: A tuple ``(node_list, relation_list)``.
            update: Passed to ``insertNode`` / ``insertRelation``.
            replace: Passed to ``insertNode`` / ``insertRelation``.
        """

    @abstractmethod
    def close(self) -> None:
        """Release resources and clear the graph store."""

    # ------------------------------------------------------------------
    # Optional vector index API (concrete default)
    # ------------------------------------------------------------------

    def enable_vector_index(
        self,
        property_name: str,
        dimensions: int,
        space: str = "cosine",
        **kwargs: Any,
    ) -> None:
        """Enable vector indexing for one property if the backend supports it.

        Backends without ANN/vector support should keep the default behavior
        and raise ``NotImplementedError``.
        """
        raise NotImplementedError(
            f"Vector indexing is not supported by {self.__class__.__name__}."
        )

    def query_vector_index(
        self,
        property_name: str,
        vector: Union[List[float], Tuple[float, ...]],
        top_k: int = 10,
    ) -> List[Tuple[int, float]]:
        """Query nearest nodes for a vector if the backend supports it."""
        raise NotImplementedError(
            f"Vector indexing is not supported by {self.__class__.__name__}."
        )

    # ------------------------------------------------------------------
    # Query helpers (concrete default — may be overridden)
    # ------------------------------------------------------------------

    def get_node(self, node_id: int) -> Optional[Node]:
        """Retrieve a node by its internal id.

        Default implementation returns None. Subclasses may override.

        Args:
            node_id: The internal node id.

        Returns:
            A ``Node`` instance, or None.
        """
        return None

    def get_node_ids(self) -> List[int]:
        """Return all internal node ids in the graph.

        Returns the backend-specific internal ids (Neo4j ``id(n)``,
        NetworkX node keys).  These are opaque identifiers and must
        not be compared with primary keys.

        Default implementation returns an empty list.
        """
        return []

    def get_node_pks(self) -> List[Dict[str, Any]]:
        """Return all primary keys of nodes in the graph.

        Each element is a dict with ``main_label`` and ``pk`` keys
        matching the ``Node`` interface.

        Default implementation returns an empty list.
        """
        return []

    def get_edges(self) -> List[Tuple[int, int, str]]:
        """Return all edges as ``(src_node_id, dst_node_id, rel_type)`` tuples.

        The node ids match what ``get_node_ids()`` returns (backend-
        specific internal ids).

        Default implementation returns an empty list.
        """
        return []

    def get_node_attrs(self, node_id: int) -> Optional[Dict[str, Any]]:
        """Return attributes stored for a node.

        Default implementation returns None.
        """
        return None

    def get_edge_attrs(self, u: int, v: int, key: str) -> Optional[Dict[str, Any]]:
        """Return attributes stored for an edge.

        Default implementation returns None.
        """
        return None

    # ------------------------------------------------------------------
    # Debug helpers (concrete default — may be overridden)
    # ------------------------------------------------------------------

    def debug(self) -> Dict[str, Any]:
        """Return a human-readable snapshot of the graph state.

        Default implementation returns an empty dict.
        """
        return {"nodes": [], "edges": [], "fk_index": {}}

    def print_debug(self) -> None:
        """Print a formatted snapshot of the graph state to stdout."""
        state = self.debug()
        print("\n=== GraphStore State ===")
        print(f"Nodes ({len(state.get('nodes', []))}):")
        for item in state.get("nodes", []):
            print(f"  {item}")
        print(f"Edges ({len(state.get('edges', []))}):")
        for item in state.get("edges", []):
            print(f"  {item}")
        print("========================\n")
