"""Karate Club dataset loader for NetworkXGraph.

Uses NetworkX's built-in Zachary Karate Club graph and maps it into DRM
nodes/relations.
"""

from __future__ import annotations

from typing import Dict

import networkx as nx

from cvcdocdb.base import Node, Relation


def load_karate_club(graph, include_club_nodes: bool = True) -> Dict[str, int]:
    """Load the built-in karate club graph into a DRM graph backend.

    Args:
        graph: Graph backend instance (typically NetworkXGraph).
        include_club_nodes: If True, creates two club nodes and MEMBER_OF edges.

    Returns:
        Dict with inserted counters.
    """
    g = nx.karate_club_graph()

    counters = {"members": 0, "clubs": 0, "interacts": 0, "member_of": 0}
    club_cache = {}

    for member_id, attrs in g.nodes(data=True):
        club_name = attrs.get("club", "Unknown")
        member = Node(
            pk={"member_id": int(member_id)},
            main_label="KarateMember",
            club=club_name,
            source="networkx.karate_club_graph",
        )
        graph.insertNode(member, replace=True)
        counters["members"] += 1

        if include_club_nodes:
            club_pk = {"club_name": club_name}
            if club_name not in club_cache:
                club_node = Node(pk=club_pk, main_label="KarateClub", name=club_name)
                graph.insertNode(club_node, replace=True)
                club_cache[club_name] = club_node
                counters["clubs"] += 1
            graph.insertRelation(Relation(member, club_cache[club_name], "MEMBER_OF"), update=True)
            counters["member_of"] += 1

    for src_id, dst_id, attrs in g.edges(data=True):
        src = Node(pk={"member_id": int(src_id)}, main_label="KarateMember")
        dst = Node(pk={"member_id": int(dst_id)}, main_label="KarateMember")
        graph.insertRelation(
            Relation(src, dst, "INTERACTS", weight=int(attrs.get("weight", 1))),
            update=True,
        )
        counters["interacts"] += 1

    return counters

