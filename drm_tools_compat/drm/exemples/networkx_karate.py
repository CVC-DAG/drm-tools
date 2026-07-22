"""DRM Tools compatibility shim for networkx_karate."""
import warnings
warnings.warn(
    "The 'drm.exemples.networkx_karate' module is deprecated.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.exemples.networkx_karate import *  # noqa: F401, F403
