"""
nx_query.py

Fluent query builder over NetworkX graphs.

Works with any NetworkX graph (``nx.DiGraph``, ``nx.MultiDiGraph``, …)
using lazy generators and a chainable API.

Usage:
    from cvcdocdb.nx_query import NxQuery
    from cvcdocdb.networkx_graph import NetworkXGraph

    g = NetworkXGraph()
    # … insert nodes …

    # Fluent query — lazy until materialised
    result = (
        g.query_nodes()
        .where({"main_label": "Person"})
        .where({"age": {"$gte": 30}})
        .limit(10)
        .to_list()
    )

    # Or use NxQuery directly on a raw NetworkX graph
    import networkx as nx
    G = nx.DiGraph()
    G.add_node("c1", tipus="Concepte", nom="valor propi", dificultat=3)
    q = NxQuery(G)
    result = q.where({"tipus": "Concepte"}).to_list()

    # Subgraph induction
    H = NxQuery(G).where({"tipus": "Concepte"}).subgraph()
    print(list(H.nodes))
"""

from __future__ import annotations

from typing import Any, Callable, Iterator, Union

from cvcdocdb.networkx_graph import _match  # MongoDB-style match logic


# ---------------------------------------------------------------------------
# Fluent query builder
# ---------------------------------------------------------------------------


class NxQuery:
    """
    Chainable, immutable (each method returns a new NxQuery) query
    over nodes or edges of a NetworkX graph.  Everything is lazy
    until you call ``to_list()``, ``ids()``, ``count()``, or ``subgraph()``.

    Parameters
    ----------
    graph : networkx.Graph
        The underlying graph (any NetworkX variant).
    items : iterator of tuple
        ``(id, attrs)`` for nodes, ``(u, v, key, attrs)`` for edges.
    kind : str
        ``"nodes"`` or ``"edges"``.
    """

    __slots__ = ("_graph", "_items", "_kind")

    def __init__(
        self,
        graph: Any,
        items: Iterator[tuple] = None,
        kind: str = "nodes",
    ) -> None:
        if kind not in ("nodes", "edges"):
            raise ValueError("kind must be 'nodes' or 'edges'")
        self._graph = graph
        self._kind = kind
        self._items = items if items is not None else self._default_iter()

    def _default_iter(self) -> Iterator[tuple]:
        if self._kind == "nodes":
            return iter(self._graph.nodes(data=True))
        return iter(self._graph.edges(data=True))

    # -- filters -------------------------------------------------------

    def where(self, query: dict) -> "NxQuery":
        """MongoDB-style declarative filter (see ``_match`` docs)."""
        def gen() -> Iterator[tuple]:
            for item in self._items:
                attrs = item[-1]  # last element is always the dict
                if _match(attrs, query):
                    yield item
        return NxQuery(self._graph, gen(), self._kind)

    def filter(self, fn: Callable) -> "NxQuery":
        """Arbitrary Python predicate filter.

        For nodes: ``fn(node_id, attrs)``.
        For edges: ``fn(u, v, key, attrs)``.
        """
        def gen() -> Iterator[tuple]:
            for item in self._items:
                if fn(*item):
                    yield item
        return NxQuery(self._graph, gen(), self._kind)

    def limit(self, n: int) -> "NxQuery":
        """Limit to the first *n* results."""
        def gen() -> Iterator[tuple]:
            for i, item in enumerate(self._items):
                if i >= n:
                    return
                yield item
        return NxQuery(self._graph, gen(), self._kind)

    # -- materialisation -----------------------------------------------

    def ids(self) -> list:
        """Per nodes: list of ids. Per edges: list of (u, v, key) tuples."""
        if self._kind == "nodes":
            return [item[0] for item in self._items]
        return [(item[0], item[1], item[2]) for item in self._items]

    def to_list(self) -> list:
        """Materialise the full result: ``(id, attrs)`` or ``(u, v, key, attrs)``."""
        return list(self._items)

    def subgraph(self) -> Any:
        """Induced subgraph from matching nodes (real copy, not zero-copy)."""
        if self._kind != "nodes":
            raise TypeError("subgraph() only makes sense for a node query")
        return self._graph.subgraph(self.ids())

    def count(self) -> int:
        """Count matching items without materialising."""
        return sum(1 for _ in self._items)

    def first(self) -> Union[tuple, None]:
        """Return the first matching item, or None."""
        return next(self._items, None)

    def __iter__(self) -> Iterator[tuple]:
        return iter(self._items)
