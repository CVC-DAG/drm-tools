"""DRM Tools compatibility shim for graph_store."""
import warnings
warnings.warn(
    "The 'drm.graph_store' module is deprecated. Use 'from cvcdocdb.graph_store import GraphStore' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.graph_store import *  # noqa: F401, F403
