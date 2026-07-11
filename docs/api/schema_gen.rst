Schema-based class generation
==============================

The :mod:`drm.schema_gen` module generates Python entity classes from a YAML
schema. It is used by :mod:`drm.rdf_schema` internally and can also be called
directly with any YAML conforming to the ``GraphStore.schema_yaml()`` format.

Usage
-----

Generate from a YAML string::

    from drm.schema_gen import generate_classes

    yaml_str = """
    labels:
      Document:
        class_name: Document
        base_class: Node
        properties:
          title: string
        primary_key: ["id"]
        doc: "A cultural document."
      Page:
        class_name: Page
        base_class: WeakNode
        properties: {}
        primary_key: []
        parent: Document
        parent_relation: HAS_PAGE
        doc: "A page within a document."
    relationships: {}
    weak_relations: {}
    """

    py_source = generate_classes(yaml_str)
    with open("drm/entities.py", "w") as f:
        f.write(py_source)

Generate from an existing graph schema::

    from drm import NetworkXGraph
    from drm.schema_gen import generate_classes

    g = NetworkXGraph()
    # ... load data ...
    yaml_str = g.schema_yaml("my_db")
    py_source = generate_classes(yaml_str)

PK detection
------------

The generator inspects the ``primary_key`` field in the YAML:

- ``primary_key: []`` (empty) → ``pk: Optional[Dict[str, Any]] = None``
- ``primary_key: ["id"]`` (non-empty) → ``pk: Dict[str, Any]`` (mandatory)

This is essential for ontologies that do not define ``owl:hasKey``: the backend
assigns an internal ID (``neo4j_id``) that becomes the effective primary key.

.. automodule:: drm.schema_gen
   :members:
   :member-order: bysource
   :show-inheritance:
