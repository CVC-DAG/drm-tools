"""DRM Tools compatibility shim for neo4j_movies."""
import warnings
warnings.warn(
    "The 'drm.exemples.neo4j_movies' module is deprecated.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.exemples.neo4j_movies import *  # noqa: F401, F403
