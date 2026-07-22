"""DRM Tools compatibility shim for neo4j_got."""
import warnings
warnings.warn(
    "The 'drm.exemples.neo4j_got' module is deprecated.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.exemples.neo4j_got import *  # noqa: F401, F403
