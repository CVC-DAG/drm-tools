Tutorials and Examples
======================

This section contains hands-on notebooks. They are rendered in the hosted
documentation when pandoc is available; otherwise they can be opened directly
from GitHub or via the links below.

Each dataset notebook shows how to load the same data into both
``NetworkXGraph`` and ``Neo4jGraph``. From every notebook page you can also
open the notebook in Google Colab, Kaggle, or a local Jupyter server.

Getting Started
---------------

Minimal end-to-end graph workflows:

- `intro_basics <notebooks/getting_started/intro_basics.ipynb>`_
- `querying_and_filtering <notebooks/getting_started/querying_and_filtering.ipynb>`_

Demos
-----

Step-by-step demonstrations covering core features:

- `delete_strategies <notebooks/demos/delete_strategies.ipynb>`_
- `propagation_demo <notebooks/demos/propagation_demo.ipynb>`_
- `ric_o_demo <notebooks/demos/ric_o_demo.ipynb>`_
- `ric_o_networkx_demo <notebooks/demos/ric_o_networkx_demo.ipynb>`_
- `vector_search <notebooks/demos/vector_search.ipynb>`_

Interactive
-----------

Hands-on explorations with Jupyter widgets:

- `weaknodes <notebooks/interactive/weaknodes.ipynb>`_

Dataset Examples
----------------

Datasets loaded into both NetworkXGraph and Neo4jGraph:

- `karate_club <notebooks/datasets/karate_club.ipynb>`_
- `bibliography_openalex <notebooks/datasets/bibliography_openalex.ipynb>`_
- `movies <notebooks/datasets/movies.ipynb>`_
- `game_of_thrones <notebooks/datasets/game_of_thrones.ipynb>`_
- `generating_classes_from_owl <notebooks/datasets/generating_classes_from_owl.ipynb>`_

Notes
-----

- Tutorials are configured to use the ``drm-tool`` Jupyter kernel by default.
- Each tutorial notebook starts with an installation cell that upgrades DRM
  from GitHub and falls back to a local editable install when needed.
- Button links can be customized with env vars: ``DRM_DOCS_GITHUB_REPO``,
  ``DRM_DOCS_GITHUB_REF``, ``DRM_DOCS_LOCAL_JUPYTER_BASE``, and
  ``DRM_DOCS_LOCAL_NOTEBOOK_PREFIX``.
