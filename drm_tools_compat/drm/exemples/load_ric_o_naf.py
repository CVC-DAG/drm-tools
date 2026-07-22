"""DRM Tools compatibility shim for load_ric_o_naf."""
import warnings
warnings.warn(
    "The 'drm.exemples.load_ric_o_naf' module is deprecated.",
    DeprecationWarning, stacklevel=2,
)
from cvcdocdb.exemples.load_ric_o_naf import *  # noqa: F401, F403
