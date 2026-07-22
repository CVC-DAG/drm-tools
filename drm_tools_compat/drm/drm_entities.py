"""DRM Tools compatibility shim for drm_entities."""
import warnings
warnings.warn(
    "The 'drm.drm_entities' module is deprecated. Use 'from cvcdocdb.drm_entities import ...' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.drm_entities import *  # noqa: F401, F403
