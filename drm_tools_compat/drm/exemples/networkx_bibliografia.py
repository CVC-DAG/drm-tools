"""DRM Tools compatibility shim for networkx_bibliografia."""
import warnings
warnings.warn(
    "The 'drm.exemples.networkx_bibliografia' module is deprecated.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.exemples.networkx_bibliografia import *  # noqa: F401, F403
