Tutorials and Examples
======================

This section contains hands-on notebooks rendered directly in the docs.

Each dataset notebook shows how to load the same data into both
``NetworkXGraph`` and ``Neo4jGraph``. From every notebook page you can also
open the notebook in Google Colab, Kaggle, or a local Jupyter server.

Getting Started
---------------

Minimal end-to-end graph workflows:

notebooks/getting_started/intro_basics
notebooks/getting_started/querying_and_filtering

Demos
-----

Step-by-step demonstrations covering core features:

notebooks/demos/delete_strategies
notebooks/demos/propagation_demo
notebooks/demos/ric_o_demo
notebooks/demos/ric_o_networkx_demo
notebooks/demos/vector_search

Interactive
-----------

Hands-on explorations with Jupyter widgets:

notebooks/interactive/weaknodes

Dataset Examples
----------------

Datasets loaded into both NetworkXGraph and Neo4jGraph:

notebooks/datasets/karate_club
notebooks/datasets/bibliography_openalex
notebooks/datasets/movies
notebooks/datasets/game_of_thrones
notebooks/datasets/generating_classes_from_owl

Notes
-----

- Notebook pages keep the original ``.ipynb`` download link in the rendered output.
- Tutorials are configured to use the ``drm-tool`` Jupyter kernel by default.
- Each tutorial notebook starts with an installation cell that upgrades DRM
  from GitHub and falls back to a local editable install when needed.
- Button links can be customized with env vars: ``DRM_DOCS_GITHUB_REPO``,
  ``DRM_DOCS_GITHUB_REF``, ``DRM_DOCS_LOCAL_JUPYTER_BASE``, and
  ``DRM_DOCS_LOCAL_NOTEBOOK_PREFIX``.
