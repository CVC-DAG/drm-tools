drm-tools (compatibility shim)
==============================

.. warning::
   This package is deprecated. Use ``cvcdocdb`` instead.

   ::

       pip install cvcdocdb

This package is a thin compatibility shim for users who still have
``import drm`` or ``pip install drm-tools`` in their code. It re-exports
everything from ``cvcdocdb`` and issues a deprecation warning on import.

Installation
------------

::

    pip install drm-tools

This will automatically install ``cvcdocdb>=1.0.0a1`` as a dependency.

Migration
---------

To migrate your code:

1. Replace ``pip install drm-tools`` with ``pip install cvcdocdb``
2. Replace ``import drm`` with ``import cvcdocdb``
3. Replace ``from drm.xxx import ...`` with ``from cvcdocdb.xxx import ...``
