DRM Tools Documentation
=======================

Document Representation Model (DRM) is a Python library for graph-based
document representation with Neo4j and an in-memory NetworkX backend.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorials/index
   api/base
   api/drm_entities
   api/neo4j_graph
   api/networkx_graph
   api/rdf_schema
   api/schema_gen

Features
--------

- **Graph-based document representation**: Model documents as nodes and
  relations, including hierarchical structures such as Document → Section → Page.
- **Two backends**: Full Neo4j integration via ``Neo4jGraph`` or an
  in-memory ``NetworkXGraph`` (NetworkX) for testing and tutorials.
- **Two entity levels**: Root entities (``Node``) and child entities
  (``WeakNode``) with composite primary keys and cascade delete
  propagation.
- **Dependency auto-insertion**: String properties (for example names) are
  automatically materialised as ``Valor`` nodes when the graph backend supports them.
- **FK validation**: Foreign key constraints on relations prevent
  dangling references.
- **ON DELETE strategies**: CASCADE, RESTRICT, SET NULL.
- **Query & filtering**: Secondary index on scalar properties, multi-filter
  search with intersection/union, and debug snapshots.
- **Vector search (NetworkX only)**: HNSW-based ANN indexing on node
  properties with ``cosine``, ``l2``, and ``ip`` distance spaces.

Primary Key
-----------

Every node must have a primary key (``pk``) or a ``neo4j_id`` (or both).
The ``pk`` is either an ``int`` or a ``dict``:

.. code-block:: python

    # Integer PK — converted to {"id": value}
    node = Node(pk=42, main_label="Document")

    # Dict PK — used as-is
    node = Node(pk={"doc_id": "DOC-001", "version": 2}, main_label="Document")

    # Auto-assigned PK — pass None explicitly; the backend generates an ID
    node = Node(pk=None, main_label="AutoIdNode")
    graph.insertNode(node)  # node._primary_key becomes {"id": <generated_id>}

    # Reconstructed from DB — neo4j_id is used as PK
    node = Node(neo4j_id=123, main_label="Document")  # _primary_key = {"id": 123}

**Rules:**

- ``Node(pk={"id": 1}, main_label="X")`` → ``_primary_key = {"id": 1}``
- ``Node(pk=42, main_label="X")`` → ``_primary_key = {"id": 42}``
- ``Node(pk=None, main_label="X")`` → ``_primary_key = None`` (backend assigns after insert)
- ``Node(pk=None, neo4j_id=123, main_label="X")`` → ``_primary_key = {"id": 123}``
- ``Node(main_label="X")`` → **ValueError** — pk must be provided

A node with ``pk=None`` is valid — the backend (Neo4j or NetworkX) assigns
an auto-generated ID as the primary key after insertion. If no backend is
used, ``_primary_key`` remains ``None``.

Query & Filtering
-----------------

``NetworkXGraph`` maintains a secondary index on scalar properties, enabling
fast lookups without scanning all nodes:

.. code-block:: python

    from drm import NetworkXGraph, Node

    graph = NetworkXGraph()
    alice = Node(pk={"name": "Alice"}, main_label="Author")
    alice["affiliation"] = "MIT"
    bob = Node(pk={"name": "Bob"}, main_label="Author")
    bob["affiliation"] = "Stanford"
    graph.insertNode(alice)
    graph.insertNode(bob)

    # Find all authors from MIT
    mit_authors = graph.find_nodes_by_property("affiliation", "MIT")
    print(mit_authors)  # [node_id_of_alice]

    # Multi-filter search (intersection or union)
    results = graph.find_nodes({"affiliation": "MIT"}, match="all")

    # Debug snapshot
    graph.print_debug()

Vector Indexing
---------------

The package exposes a common vector-index API on graph stores:

- ``enable_vector_index(property_name, dimensions, space="cosine", ...)``
- ``query_vector_index(property_name, vector, top_k=10)``

Current backend support:

- ``NetworkXGraph``: supported (uses ``hnswlib``)
- ``Neo4jGraph``: API is present but currently raises ``NotImplementedError``

Example (``NetworkXGraph``):

.. code-block:: python

    from drm import NetworkXGraph, Node

    graph = NetworkXGraph()
    graph.enable_vector_index("embedding", dimensions=3, space="cosine")

    graph.insertNode(Node(pk={"id": 1}, main_label="Doc", embedding=[1.0, 0.0, 0.0]), replace=True)
    graph.insertNode(Node(pk={"id": 2}, main_label="Doc", embedding=[0.0, 1.0, 0.0]), replace=True)

    results = graph.query_vector_index("embedding", [1.0, 0.0, 0.0], top_k=2)
    print(results)  # [(node_id, distance), ...]
    graph.close()

Installation
------------

Install the package in development mode:

.. code-block:: bash

    pip install -e .

Quick Start
-----------

.. code-block:: python

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

For the in-memory backend:

.. code-block:: python

    from drm import NetworkXGraph, Node

    graph = NetworkXGraph()
    doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
    graph.insertNode(doc)
    print(graph.get_node_ids())  # [1]
    graph.close()

Configuration
-------------

DRM uses environment variables for Neo4j connections. Multiple targets are
supported via the ``NEO4J_TARGET`` selector:

.. code-block:: bash

    export NEO4J_DEV_URL=bolt://dev-host:7687
    export NEO4J_DEV_USER=neo4j
    export NEO4J_DEV_PASSWORD=your_dev_password
    export NEO4J_DEV_DATABASE=neo4j

For a custom target:

.. code-block:: bash

    export NEO4J_TARGET=LOCAL
    export NEO4J_LOCAL_URL=bolt://localhost:7687
    export NEO4J_LOCAL_USER=neo4j
    export NEO4J_LOCAL_PASSWORD=your_password
    export NEO4J_LOCAL_DATABASE=neo4j

The real Neo4j tests default to ``DEV`` when ``NEO4J_TARGET`` is not set,
and fall back to plain ``NEO4J_*`` variables when prefixed variables are absent.

Running Tests
-------------

Run the test suite with pytest:

.. code-block:: bash

    python -m pytest test/ -v

Tests use ``NetworkXGraph`` for all unit tests and ``Neo4jGraph`` for
integration tests against a real Neo4j instance (controlled by ``NEO4J_TARGET``).

Building Documentation
----------------------

Generate the HTML documentation with Sphinx:

.. code-block:: bash

    cd docs
    sphinx-build -b html . _build/html

Or use the virtual environment:

.. code-block:: bash

    .venv/bin/sphinx-build -b html docs/ docs/_build/html/

Authors
-------

- Oriol Ramos Terrades
- Jialuo Chen
- Adrià Molina

Acknowledgements
----------------

This work has been partially supported by the Spanish project
PID2021-126808OB-I00, Ministerio de Ciencia e Innovación, the Departament
de Cultura of the Generalitat de Catalunya, and the CERCA Program /
Generalitat de Catalunya. Adrià Molina is funded with the PRE2022-101575
grant provided by MCIN / AEI / 10.13039 / 501100011033 and by the
European Social Fund (FSE+).
