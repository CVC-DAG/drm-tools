"""DRM Tools compatibility shim for cli."""
import warnings
warnings.warn(
    "The 'drm.exemples.cli' module is deprecated.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.exemples.cli import *  # noqa: F401, F403
