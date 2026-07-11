# Document Representation Model (drm-tools)

Graph-based document representation library with Neo4j and an in-memory NetworkX backend.

Model documents as graphs where nodes represent document objects (text regions, figures, pages) and edges capture their relationships. The library supports semantic entity definitions, weak nodes with cascade delete, foreign key validation, and reusable example datasets for tutorials.

## Features

- **Two backends**: Full Neo4j integration (`Neo4jGraph`) or in-memory NetworkX (`NetworkXGraph`) for testing and tutorials
- **Two entity levels**: Root entities (`Node`) and child entities (`WeakNode`) with composite primary keys and cascade delete
- **ON DELETE strategies**: CASCADE, RESTRICT, SET NULL
- **Semantic entities**: Domain-specific node types such as `IndividuPadro`, `LlocPadro`, and `Fotografia`
- **FK validation**: Foreign key constraints on relations prevent dangling references
- **Vector index API (optional)**: Common `GraphStore` methods for ANN-style vector indexing by property

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
from drm import Neo4jGraph, Node, WeakNode

# Connect to Neo4j
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    user="neo4j",
    password="secret",
    database="mydb",
)

# Create a document hierarchy
doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
graph.insertNode(doc, replace=True)

section = WeakNode(parent=doc, pk={"section": 1}, main_label="Section")
graph.insertNode(section, insert_parent=True)

page = WeakNode(parent=section, pk={"page": 1}, main_label="Page")
graph.insertNode(page, insert_parent=True)

graph.close()
```

## Example Dataset Loaders (`drm/exemples`)

The package includes ready-to-run loaders for common graph domains:

- `drm.exemples.networkx_karate`: Karate Club graph (NetworkX classic)
- `drm.exemples.networkx_bibliografia`: bibliographic references from OpenAlex
- `drm.exemples.neo4j_movies`: movie-domain graph for Neo4j
- `drm.exemples.neo4j_got`: Game of Thrones character-house graph for Neo4j

The tutorial notebooks use the same four loaders with both backends, so you
can compare the NetworkX and Neo4j results side by side (4 datasets × 2 backends).

The docs split the tutorials into dataset-specific notebooks:

- `Karate Club`
- `Bibliographic references`
- `Movies`
- `Game of Thrones`

### Command-line loader

You can also load datasets from the terminal:

```bash
python -m drm.exemples --dataset karate --backend networkx
python -m drm.exemples --dataset all --backend both --quiet
```

Minimal usage:

```python
from drm import NetworkXGraph
from drm.exemples import load_karate_club, load_bibliografia_openalex

graph = NetworkXGraph()
print(load_karate_club(graph))
print(load_bibliografia_openalex(graph, query="graph database", per_page=15))
graph.close()
```


## Configuration

Create a `.env` file with your Neo4j credentials:

```
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=mydb
```

For multiple Neo4j instances, you can use a target selector.
The test suite defaults to the `DEV` target when `NEO4J_TARGET` is not set:

```bash
NEO4J_TARGET=LOCAL

NEO4J_LOCAL_URL=bolt://localhost:7687
NEO4J_LOCAL_USER=neo4j
NEO4J_LOCAL_PASSWORD=your_password
NEO4J_LOCAL_DATABASE=neo4j

NEO4J_DEV_URL=bolt://dev-host:7687
NEO4J_DEV_USER=neo4j
NEO4J_DEV_PASSWORD=your_dev_password
NEO4J_DEV_DATABASE=neo4j
```

The real Neo4j tests (`test/test_neo4j_real.py`, `test/test_graph_store_contract.py`,
and `test/test_create_graph.py`) will use `NEO4J_TARGET` if set, default to
`DEV` otherwise, and fall back to plain `NEO4J_*` variables when present.

## Running Tests

```bash
python -m pytest test/ -v
```

## Documentation

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
