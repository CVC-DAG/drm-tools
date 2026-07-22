"""DRM Tools compatibility shim for exemples."""
import warnings
warnings.warn(
    "The 'drm.exemples' package is deprecated. Use 'from cvcdocdb.exemples import ...' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.exemples.cli import *  # noqa: F401, F403
from cvcdocdb.exemples.load_ric_o_naf import *  # noqa: F401, F403
from cvcdocdb.exemples.neo4j_got import *  # noqa: F401, F403
from cvcdocdb.exemples.neo4j_movies import *  # noqa: F401, F403
from cvcdocdb.exemples.networkx_bibliografia import *  # noqa: F401, F403
from cvcdocdb.exemples.networkx_karate import *  # noqa: F401, F403
