"""DRM Tools compatibility shim for networkx_graph."""
import warnings
warnings.warn(
    "The 'drm.networkx_graph' module is deprecated. Use 'from cvcdocdb.networkx_graph import NetworkXGraph' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.networkx_graph import *  # noqa: F401, F403
