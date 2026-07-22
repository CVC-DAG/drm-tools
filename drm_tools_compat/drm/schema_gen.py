"""DRM Tools compatibility shim for schema_gen."""
import warnings
warnings.warn(
    "The 'drm.schema_gen' module is deprecated. Use 'from cvcdocdb.schema_gen import ...' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.schema_gen import *  # noqa: F401, F403
