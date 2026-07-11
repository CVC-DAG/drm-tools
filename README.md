# Document Representation Model (drm-tools)

Graph-based document representation library with Neo4j and an in-memory NetworkX backend.

Model documents as graphs where nodes represent document objects (text regions, figures, pages) and edges capture their relationships. The library supports semantic entity definitions, weak nodes with cascade delete, foreign key validation, vector search, and reusable example datasets for tutorials.

## Features

- **Two backends**: Full Neo4j integration (`Neo4jGraph`) or in-memory NetworkX (`NetworkXGraph`) for testing and tutorials
- **WeakNode hierarchy**: Child entities with composite primary keys and automatic cascade delete through parent-child edges
- **ON DELETE strategies**: CASCADE, RESTRICT, SET NULL — choose the deletion semantics that fit your use case
- **Semantic entities**: Domain-specific node types such as `IndividuPadro`, `LlocPadro`, and `Fotografia`
- **FK validation**: Foreign key constraints on relations prevent dangling references
- **Query & filtering**: Secondary index on scalar properties, multi-filter search with intersection/union, debug snapshots
- **Vector search (NetworkX only)**: HNSW-based ANN indexing on node properties with `cosine`, `l2`, and `ip` distance spaces

## Installation

```bash
pip install -e .
```

Register the recommended Jupyter kernel for tutorials:

```bash
python -m ipykernel install --user --name drm-tool --display-name "Python (drm-tool)"
```

## Quick Start

```python
from drm import NetworkXGraph, Node, WeakNode

# In-memory backend — no database required
graph = NetworkXGraph()

# Create a document hierarchy
doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
graph.insertNode(doc)

section = WeakNode(parent=doc, pk={"section": 1}, main_label="Section")
graph.insertNode(section, insert_parent=True)

page = WeakNode(parent=section, pk={"page": 1}, main_label="Page")
graph.insertNode(page, insert_parent=True)

# Query the graph
print("Nodes:", graph.get_node_ids())
print("Edges:", graph.get_edges())
graph.close()
```

## Tutorial Notebooks

The `docs/tutorials/notebooks/` directory contains runnable examples organized by topic:

### Getting Started

- **`intro/intro_basics.ipynb`** — Minimal end-to-end workflow: insert nodes, create WeakNode hierarchies
- **`intro/querying_and_filtering.ipynb`** — Query operations: `get_node()`, `find_nodes()`, property filtering, debug snapshots

### Interactive Demos

- **`interactive/weaknodes_interactive.ipynb`** — Build Document → Section → Page hierarchies with an interactive widget panel
- **`interactive/vector_search.ipynb`** — HNSW vector indexing and nearest-neighbor search on node properties
- **`interactive/delete_strategies.ipynb`** — Compare CASCADE, RESTRICT, SET NULL deletion strategies with WeakNode cascade propagation

### Dataset Examples

Each dataset loads into both backends for side-by-side comparison:

- **`datasets/karate_club.ipynb`** — Zachary Karate Club (34 members, community detection)
- **`datasets/movies.ipynb`** — Movie-domain graph (actors, genres, films)
- **`datasets/game_of_thrones.ipynb`** — Character-house graph
- **`datasets/bibliography_openalex.ipynb`** — OpenAlex bibliographic references with citation links

## Example Dataset Loaders (`drm.exemples`)

The package includes ready-to-run loaders for common graph domains:

- `drm.exemples.networkx_karate`: Karate Club graph (NetworkX classic)
- `drm.exemples.networkx_bibliografia`: bibliographic references from OpenAlex
- `drm.exemples.neo4j_movies`: movie-domain graph
- `drm.exemples.neo4j_got`: Game of Thrones character-house graph

### Command-line loader

```bash
python -m drm.exemples --dataset karate --backend networkx
python -m drm.exemples --dataset all --backend both --quiet
```

### Programmatic usage

```python
from drm import NetworkXGraph
from drm.exemples import load_karate_club, load_bibliografia_openalex

graph = NetworkXGraph()
print(load_karate_club(graph))
print(load_bibliografia_openalex(graph, query="graph database", per_page=15))
graph.close()
```

## Configuration

DRM uses environment variables for Neo4j connections. Multiple targets are supported via the `NEO4J_TARGET` selector:

```bash
# Default target (used when NEO4J_TARGET is not set)
export NEO4J_DEV_URL=bolt://dev-host:7687
export NEO4J_DEV_USER=neo4j
export NEO4J_DEV_PASSWORD=your_dev_password
export NEO4J_DEV_DATABASE=neo4j
```

For a custom target:

```bash
export NEO4J_TARGET=LOCAL
export NEO4J_LOCAL_URL=bolt://localhost:7687
export NEO4J_LOCAL_USER=neo4j
export NEO4J_LOCAL_PASSWORD=your_password
export NEO4J_LOCAL_DATABASE=neo4j
```

The real Neo4j tests (`test/test_neo4j_real.py`, `test/test_graph_store_contract.py`) default to `DEV` when `NEO4J_TARGET` is not set, and fall back to plain `NEO4J_*` variables when prefixed variables are absent.

## Running Tests

```bash
python -m pytest test/ -v
```

Tests use `NetworkXGraph` for all unit tests and `Neo4jGraph` for integration tests against a real Neo4j instance (controlled by `NEO4J_TARGET`).

## Documentation

- **Source docs**: [docs/](docs/) — Sphinx documentation source
- **Tutorials**: [docs/tutorials/notebooks/](docs/tutorials/notebooks/) — Jupyter notebook examples

Generate HTML docs with Sphinx:

```bash
cd docs
sphinx-build -b html . _build/html
```

Or use the virtual environment:

```bash
.venv/bin/sphinx-build -b html docs/ docs/_build/html/
```

## Authors & Contributors

- Oriol Ramos Terrades
- Jialuo Chen
- Adrià Molina

## Acknowledgements

This work has been partially supported by the Spanish project PID2021-126808OB-I00, Ministerio de Ciencia e Innovación, the Departament de Cultura of the Generalitat de Catalunya, and the CERCA Program / Generalitat de Catalunya. Adrià Molina is funded with the PRE2022-101575 grant provided by MCIN / AEI / 10.13039 / 501100011033 and by the European Social Fund (FSE+).
