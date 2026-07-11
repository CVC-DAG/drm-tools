"""Command-line interface for the tutorial/example datasets.

This CLI lets you load any of the bundled example datasets into either the
in-memory NetworkX backend or Neo4j.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Callable, Dict

from drm import Neo4jGraph, NetworkXGraph

from .networkx_karate import load_karate_club
from .networkx_bibliografia import load_bibliografia_openalex
from .neo4j_movies import load_movies_sample
from .neo4j_got import load_got_characters


DATASETS: dict[str, dict[str, Any]] = {
    "karate": {
        "loader": load_karate_club,
        "description": "Zachary karate club benchmark",
        "kwargs": {},
    },
    "bibliography": {
        "loader": load_bibliografia_openalex,
        "description": "OpenAlex bibliographic sample",
        "kwargs": {"query": "graph database", "per_page": 15},
    },
    "movies": {
        "loader": load_movies_sample,
        "description": "Movie-domain sample",
        "kwargs": {"limit": 25},
    },
    "got": {
        "loader": load_got_characters,
        "description": "Game of Thrones-style character sample",
        "kwargs": {"limit": 25},
    },
}


def neo4j_config(default_target: str = "DEV") -> Dict[str, str]:
    target = os.environ.get("NEO4J_TARGET", default_target).upper()
    prefix = f"NEO4J_{target}_"
    return {
        "target": target,
        "url": os.environ.get(f"{prefix}URL", os.environ.get("NEO4J_URL", "bolt://localhost:7687")),
        "user": os.environ.get(f"{prefix}USER", os.environ.get("NEO4J_USER", "neo4j")),
        "password": os.environ.get(f"{prefix}PASSWORD", os.environ.get("NEO4J_PASSWORD", "secret")),
        "database": os.environ.get(f"{prefix}DATABASE", os.environ.get("NEO4J_DATABASE", "neo4j")),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m drm.exemples",
        description="Load tutorial/example datasets into NetworkX or Neo4j.",
    )
    parser.add_argument(
        "--backend",
        choices=("networkx", "neo4j", "both"),
        default="networkx",
        help="Target backend to load into (default: networkx).",
    )
    parser.add_argument(
        "--dataset",
        choices=("karate", "bibliography", "movies", "got", "all"),
        default="all",
        help="Dataset to load (default: all).",
    )
    parser.add_argument("--query", default="graph database", help="OpenAlex query for bibliography.")
    parser.add_argument("--per-page", type=int, default=15, help="Number of OpenAlex works to fetch.")
    parser.add_argument("--limit", type=int, default=25, help="Limit for movies/GOT sample loaders.")
    parser.add_argument("--mailto", default=None, help="Optional OpenAlex mailto parameter.")
    parser.add_argument("--quiet", action="store_true", help="Only print the final JSON summary.")
    return parser


def _dataset_kwargs(name: str, args: argparse.Namespace) -> Dict[str, Any]:
    info = DATASETS[name]
    kwargs = dict(info["kwargs"])
    if name == "bibliography":
        kwargs.update({"query": args.query, "per_page": args.per_page, "mailto": args.mailto})
    elif name in ("movies", "got"):
        kwargs.update({"limit": args.limit})
    return kwargs


def _load_into_backend(backend: str, name: str, args: argparse.Namespace) -> Dict[str, Any]:
    info = DATASETS[name]
    loader: Callable[..., Dict[str, int]] = info["loader"]
    kwargs = _dataset_kwargs(name, args)

    if backend == "networkx":
        graph = NetworkXGraph()
        backend_label = "NetworkXGraph"
    else:
        cfg = neo4j_config()
        graph = Neo4jGraph(
            url=cfg["url"],
            user=cfg["user"],
            password=cfg["password"],
            database=cfg["database"],
        )
        backend_label = f"Neo4jGraph(target={cfg['target']})"

    try:
        result = loader(graph, **kwargs)
    finally:
        graph.close()

    return {
        "backend": backend_label,
        "dataset": name,
        "description": info["description"],
        "result": result,
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    datasets = list(DATASETS) if args.dataset == "all" else [args.dataset]
    backends = [args.backend] if args.backend != "both" else ["networkx", "neo4j"]

    summaries = []
    for backend in backends:
        for name in datasets:
            summary = _load_into_backend(backend, name, args)
            summaries.append(summary)
            if not args.quiet:
                print(f"[{backend}] {name}: {summary['result']}")

    print(json.dumps(summaries, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

