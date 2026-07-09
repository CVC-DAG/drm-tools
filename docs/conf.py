# Configuration file for the Sphinx documentation builder.
#
# For the full list of built configurations, see the Sphinx docs:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the project root to the path so Sphinx can find the drm package.
sys.path.insert(0, os.path.abspath(os.path.join("..")))

# -- Project information -----------------------------------------------------
project = "DRM Tools"
copyright = "2025, Oriol Ramos Terrades, Jialuo Chen, Adrià Molina"
author = "Oriol Ramos Terrades, Jialuo Chen, Adrià Molina"

# The full version, including alpha/beta/rc tags
try:
    from drm import __version__ as drm_version  # noqa: E402
except ImportError:
    drm_version = None

release = drm_version if drm_version else "1.0"
version = release

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",       # Auto-generate docs from docstrings
    "sphinx.ext.napoleon",      # Google and NumPy style docstring support
    "sphinx.ext.viewcode",      # Add links to highlighted source code
    "sphinx.ext.intersphinx",   # Link to other projects' documentation
    # "sphinx_autodoc_typehints" — disabled: crashes on dict-inherited descriptors
]

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": (
        "__weakref__, pk, keys, values, items, __getitem__,"
        " __setitem__, __delitem__, __contains__, __len__,"
        " __iter__, __eq__, __hash__, copy, clear,"
        " pop, popitem, update, fromkeys, get"
    ),
}
autodoc_typehints = "description"  # Show types in descriptions, not signatures
autodoc_typehints_description_target = "all"

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
}

# Templates path
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Theme options
html_theme_options = {
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {}
latex_documents = [
    (
        "index",
        "drm-tools.tex",
        "DRM Tools Documentation",
        "Oriol Ramos Terrades, Jialuo Chen, Adrià Molina",
        "manual",
    ),
]

# Skip sphinx-autodoc-typehints processing for properties and descriptors
# that cause "'getset_descriptor' object is not iterable" errors.
def _autodoc_skip_member(app, what, name, obj, skip, options):
    """Skip private members, properties and built-in descriptors from autodoc."""
    # Keep __init__, skip everything else starting with _
    if name.startswith("_") and name != "__init__":
        return True
    # Skip property descriptors that crash sphinx-autodoc-typehints
    if isinstance(obj, property) or type(obj).__name__ in (
        "getset_descriptor", "member_descriptor",
    ):
        return True
    return None  # let default logic decide

def _skip_properties_docstring(app, what, name, obj, options, lines):
    """Remove auto-generated :ivar: lines for properties."""
    if what in ("attribute", "property") or isinstance(obj, property):
        del lines[:]

def setup(app):
    app.connect("autodoc-skip-member", _autodoc_skip_member)
    app.connect("autodoc-process-docstring", _skip_properties_docstring)

# -- Options for manual page output ------------------------------------------
man_pages = [
    (
        "index",
        "drm-tools",
        "DRM Tools Documentation",
        ["Oriol Ramos Terrades, Jialuo Chen, Adrià Molina"],
        1,
    ),
]
