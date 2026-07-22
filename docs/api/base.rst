Core primitives
===============

The :mod:`cvcdocdb.base` module defines the low-level graph primitives used
throughout the library:

- :class:`~cvcdocdb.base.Node` for root entities
- :class:`~cvcdocdb.base.WeakNode` for hierarchical child entities
- :class:`~cvcdocdb.base.Relation` for typed edges
- :class:`~cvcdocdb.base.WeakRelation` for parent-child cascade relations

These classes are the foundation for both backends and for all semantic
entities defined in :mod:`cvcdocdb.drm_entities`.

See also :mod:`cvcdocdb.networkx_graph` and :mod:`cvcdocdb.neo4j_graph` for the concrete
backends that consume these primitives.

.. automodule:: cvcdocdb.base
   :members:
   :member-order: bysource
   :show-inheritance:
