# Document Representation Model (drm-tools)

Graph-based document representation library with Neo4j and in-memory backends.

Model documents as graphs where nodes represent document objects (text regions, figures, pages) and edges capture their relationships. Supports semantic entity definitions, weak nodes with cascade delete, and foreign key validation.

## Features

- **Two backends**: Full Neo4j integration (`Neo4jGraph`) or in-memory NetworkX (`NetworkXGraph`) for testing
- **Two entity levels**: Root entities (`Node`) and child entities (`WeakNode`) with composite primary keys and cascade delete
- **ON DELETE strategies**: CASCADE, RESTRICT, SET NULL
- **Semantic entities**: Domain-specific node types (IndividuPadro, LlocPadro, Fotografia, etc.)
- **FK validation**: Foreign key constraints on relations prevent dangling references

## Installation

```bash
pip install -e .
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

For the in-memory backend:

```python
from drm import NetworkXGraph, Node

graph = NetworkXGraph()
doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
graph.insertNode(doc, replace=True)
print(graph.get_nodes())  # {1}
graph.close()
```

## Primary Key

Every node must have a primary key (`pk`) or a `neo4j_id` (or both). The `pk` is either an `int` or a `dict`:

```python
# Integer PK — converted to {"id": value}
node = Node(pk=42, main_label="Document")

# Dict PK — used as-is
node = Node(pk={"doc_id": "DOC-001", "version": 2}, main_label="Document")

# Auto-assigned PK — pass None explicitly; the backend generates an ID
node = Node(pk=None, main_label="AutoIdNode")
graph.insertNode(node)  # node._primary_key becomes {"id": <generated_id>}

# Reconstructed from DB — neo4j_id is used as PK
node = Node(neo4j_id=123, main_label="Document")  # _primary_key = {"id": 123}
```

**Rules:**

| Constructor call | `_primary_key` |
|---|---|
| `Node(pk={"id": 1}, main_label="X")` | `{"id": 1}` |
| `Node(pk=42, main_label="X")` | `{"id": 42}` |
| `Node(pk=None, main_label="X")` | `None` → backend assigns after insert |
| `Node(pk=None, neo4j_id=123, main_label="X")` | `{"id": 123}` |
| `Node(main_label="X")` | **`ValueError`** — pk must be provided |

A node with `pk=None` is valid — the backend (Neo4j or NetworkX) assigns an auto-generated ID as the primary key after insertion. If no backend is used, `_primary_key` remains `None`.

## Configuration

Create a `.env` file with your Neo4j credentials:

```
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=mydb
```

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
