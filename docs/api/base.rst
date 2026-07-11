Core primitives
===============

The :mod:`drm.base` module defines the low-level graph primitives used
throughout the library:

- :class:`~drm.base.Node` for root entities
- :class:`~drm.base.WeakNode` for hierarchical child entities
- :class:`~drm.base.Relation` for typed edges
- :class:`~drm.base.WeakRelation` for parent-child cascade relations

These classes are the foundation for both backends and for all semantic
entities defined in :mod:`drm.drm_entities`.

See also :mod:`drm.networkx_graph` and :mod:`drm.neo4j_graph` for the concrete
backends that consume these primitives.

.. automodule:: drm.base
   :members:
   :member-order: bysource
   :show-inheritance:
