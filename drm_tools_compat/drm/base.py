"""DRM Tools compatibility shim for base."""
import warnings
warnings.warn(
    "The 'drm.base' module is deprecated. Use 'from cvcdocdb.base import ...' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.base import *  # noqa: F401, F403
