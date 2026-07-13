# Document Representation Model (drm-tools)

Graph-based document representation library with Neo4j and an in-memory NetworkX backend.

`drm-tools` implements the **Document Representation Model**, developed as part of the **SUKIDI** research project (*Semantic Understanding and Knowledge Integration for Document Intelligence*). The project is based on the hypothesis that integrating **contextual knowledge** (declarative and procedural) into document intelligence systems significantly improves their interpretation capabilities, overcoming the limitations of current foundation models that work well with structured documents but struggle with historical, graphical, or diagrammatic documents.

Model documents as graphs where nodes capture document objects (text regions, figures, pages) and edges model their semantic and hierarchical relationships. This enables the integration of **declarative knowledge** (semantic entities defined within the graph domain) and **procedural knowledge** (cascade delete strategies, foreign key validation) over the same structure. The package supports two backends: `Neo4jGraph` for persistent storage and `NetworkXGraph` for in-memory testing, and includes tools to convert RDF/OWL ontologies (such as RiC-O) into Python classes, facilitating domain-specific knowledge integration. Additional backends are planned for future releases.

Target applications include administrative document processing (RPA), historical archives (such as the National Census of Victims), manuscripts with rare scripts, and graphical languages (music scores, engineering drawings).

## Features

- **Two backends**: Full Neo4j integration (`Neo4jGraph`) or in-memory NetworkX (`NetworkXGraph`)
- **WeakNode hierarchy**: Child entities with composite primary keys and automatic cascade delete
- **ON DELETE strategies**: CASCADE, RESTRICT, SET NULL
- **Transactional group creation**: `create_group()` inserts a strong node with its WeakNodes atomically
- **Fluent query builder**: `NxQuery` chainable API over NetworkX graphs with lazy generators
- **Vector search (NetworkX only)**: HNSW-based ANN indexing with `cosine`, `l2`, and `ip` distance spaces
- **RDF/OWL ontology conversion**: Generate Python entity classes from RDF/OWL ontologies

## Installation

```bash
pip install drm-tools
```

Or from source:

```bash
git clone https://github.com/CVC-DAG/drm-tools.git
cd drm-tools
pip install -e .
```

## Quick Start

```python
from drm import NetworkXGraph, Node, WeakNode

graph = NetworkXGraph()

doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
graph.insertNode(doc)

section = WeakNode(parent=doc, pk={"section": 1}, main_label="Section")
graph.insertNode(section, insert_parent=True)

page = WeakNode(parent=section, pk={"page": 1}, main_label="Page")
graph.insertNode(page, insert_parent=True)

print("Nodes:", graph.get_node_ids())
print("Edges:", graph.get_edges())
graph.close()
```

## Tutorials

Runnable Jupyter notebooks in [`docs/tutorials/notebooks/`](docs/tutorials/notebooks/). Hosted documentation at [cvc-dag.github.io/drm-tools](https://cvc-dag.github.io/drm-tools/).

- **Getting started**: basics, querying, filtering
- **Demos**: vector search, delete strategies, RiC-O loader, propagation demo
- **Datasets**: Karate Club, Movies, Game of Thrones, OpenAlex bibliography
- **Ontologies**: generating Python classes from RDF/OWL

## Configuration

DRM uses environment variables for Neo4j connections. See [`.env.example`](.env.example) for a complete template.

```bash
export NEO4J_DEV_URL=bolt://localhost:7687
export NEO4J_DEV_USER=neo4j
export NEO4J_DEV_PASSWORD=default
export NEO4J_DEV_DATABASE=neo4j
```

## Tests

```bash
python -m pytest test/ -v
```

Three levels: **Unit** (`-m unit`), **Integration** (`-m integration`, NetworkX), **Neo4j** (`-m slow`). See [`test/README.md`](test/README.md) for details.

## Documentation

- **Hosted**: https://cvc-dag.github.io/drm-tools/
- **Source**: [`docs/`](docs/) -- `sphinx-build -b html docs/ docs/_build/html/`
- **Example loaders**: `python -m drm.exemples --dataset all --backend both`

## Authors

- Oriol Ramos Terrades — oriolrt@cvc.uab.cat
- Jialuo Chen — jchen@cvc.uab.cat
- Adrià Molina — amolina@cvc.uab.cat

## Acknowledgements

Partially supported by the Spanish project PID2024-157778OB-I00 (Ministerio de Ciencia e Innovación), the Departament de Cultura of the Generalitat de Catalunya, and the CERCA Program / Generalitat de Catalunya. Adrià Molina is funded with the PRE2022-101575 grant (MCIN / AEI / 10.13039 / 501100011033 and FSE+).
