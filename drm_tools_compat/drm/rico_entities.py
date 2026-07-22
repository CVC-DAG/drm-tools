"""DRM Tools compatibility shim for rico_entities."""
import warnings
warnings.warn(
    "The 'drm.rico_entities' module is deprecated. Use 'from cvcdocdb.rico_entities import ...' instead.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.rico_entities import *  # noqa: F401, F403
