"""DRM Tools compatibility shim for neo4j_graph."""
import warnings
warnings.warn(
    "The 'drm.neo4j_graph' module is deprecated. Use 'from cvcdocdb.neo4j_graph import Neo4jGraph' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.neo4j_graph import *  # noqa: F401, F403
