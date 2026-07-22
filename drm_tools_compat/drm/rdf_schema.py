"""DRM Tools compatibility shim for rdf_schema."""
import warnings
warnings.warn(
    "The 'drm.rdf_schema' module is deprecated. Use 'from cvcdocdb.rdf_schema import ...' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.rdf_schema import *  # noqa: F401, F403
