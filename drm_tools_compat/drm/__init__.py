"""DRM Tools compatibility shim.

This package is a thin compatibility layer for users still importing
``drm`` instead of ``cvcdocdb``. It re-exports everything from ``cvcdocdb``
and issues a deprecation warning on first import.

.. deprecated:: 1.0.0a1
    Use ``import cvcdocdb`` instead. This shim will be removed in a future release.
"""

import warnings

warnings.warn(
    "The 'drm' package is deprecated and will be removed in a future release. "
    "Use 'import cvcdocdb' instead. "
    "Install with: pip install cvcdocdb",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from cvcdocdb
from cvcdocdb.base import *  # noqa: F401, F403
from cvcdocdb.drm_entities import *  # noqa: F401, F403
from cvcdocdb.graph_store import GraphStore  # noqa: F401
from cvcdocdb.schema_gen import *  # noqa: F401, F403

__version__ = "1.0.0a1"


def __getattr__(name):
    """Lazy import for optional backend modules."""
    if name == "Neo4jGraph":
        from cvcdocdb.neo4j_graph import Neo4jGraph
        return Neo4jGraph
    if name == "NetworkXGraph":
        from cvcdocdb.networkx_graph import NetworkXGraph
        return NetworkXGraph
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


try:
    from cvcdocdb.base import __all__ as _base_all
    if _base_all:
        __all__ = _base_all
except ImportError:
    __all__ = []
