# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

- **`_UNSET` duplicate in `base.py`** — Removed duplicate `_UNSET` sentinel constant (was defined at lines 12 and 78).

### Documentation

- _No changes yet._

## [1.1.0rc2] - 2026-07-11

### Added

- **Tutorial notebooks: querying & filtering** — `docs/tutorials/notebooks/intro/querying_and_filtering.ipynb` demonstrates `get_node()`, `get_node_attrs()`, `get_edge_attrs()`, `get_node_pks()`, `find_nodes_by_property()`, `find_nodes()`, and `debug()`/`print_debug()`.
- **Tutorial notebook: vector search** — `docs/tutorials/notebooks/interactive/vector_search.ipynb` demonstrates `enable_vector_index()` with cosine/l2/ip distance spaces and `query_vector_index()` on a worked example.
- **Tutorial notebook: delete strategies** — `docs/tutorials/notebooks/interactive/delete_strategies.ipynb` demonstrates CASCADE, RESTRICT, and SET NULL strategies with WeakNode cascade propagation.

### Changed

- **Method ordering in all graph classes** — Reordered `__init__`, public methods (CRUD → query → lifecycle), protected helpers, and static helpers in `Neo4jGraph`, `NetworkXGraph`, `Node`, and `Relation` following Python best practices (PEP 8 convention).
- **`README.md` completely rewritten** — Added vector search and query/filtering features, restructured tutorial notebooks into three categories (Getting Started, Interactive Demos, Dataset Examples), updated configuration to use `NEO4J_TARGET` env var selector, simplified Quick Start to use `NetworkXGraph`.
- **`docs/index.rst` completely rewritten** — Added Features, Query & Filtering, and Vector Indexing sections; updated Configuration to use `NEO4J_TARGET`; updated Quick Start with both backends; added Authors and Acknowledgements.
- **Tutorial notebook organisation** — Removed `legacy/` directory and its notebooks (`neo4j_backend.ipynb`, `networkx_backend.ipynb`). Reorganised tutorials into `intro/`, `interactive/`, and `datasets/` subdirectories.

### Fixed

- **Removed session artifacts** — Deleted `CHANGELOG_NEO4J_TESTS.md`, `DEV_CONFIG_UPDATE.md`, `QUICKSTART_NEO4J_DEV.md`, `REVIEW_NEO4J_TESTS.md`, `TEST_REVIEW_SUMMARY.md` (temporary markdown files from previous sessions).

### Documentation

- **Tutorial index** — `docs/tutorials/index.rst` updated: removed "Legacy tutorials" section, added `querying_and_filtering` to Introductory, added `vector_search` and `delete_strategies` to Interactive Demos, renamed "Dataset-specific" to "Dataset Examples".

## [1.1.0rc1] - 2026-07-11

### Added

- **`GraphStore` ABC** (`drm/graph_store.py`) — Abstract base class defining the interface for all graph backends. Declares 6 abstract methods (`insertNode`, `insertRelation`, `deleteNode`, `checkNode`, `create`, `close`) and provides concrete default implementations for helper methods (`get_node`, `get_nodes`, `get_edges`, `get_node_attrs`, `get_edge_attrs`, `debug`, `print_debug`).
- **Contract tests** (`test/test_graph_store_contract.py`) — 21 test methods verifying propagation policies (ON DELETE CASCADE, RESTRICT, SET NULL, ON UPDATE CASCADE), WeakNode composite PKs, cascade delete, FK violations, replace behaviour, bulk import, checkNode, duplicate key, and close safety. `TestNetworkXGraph` runs all 21; `TestNeo4jGraph` runs against a real database when `NEO4J_URL`/`NEO4J_USER`/`NEO4J_PASSWORD` are set.
- **`pk=None` explicit parameter** — `Node(pk=None, main_label="X")` creates a node with `_primary_key = None`. The backend (Neo4jGraph or NetworkXGraph) assigns an auto-generated ID as the primary key after insertion. Passing `pk` without a value (not even `None`) still raises `ValueError`.
- **`.env` file** — Template with Neo4j connection settings (NEO4J_URL, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE). Listed in `.gitignore`.
- **`NetworkXGraph` transparent persistence** — The graph store now always persists state to disk and reloads it automatically on initialization. This makes in-memory usage restart-safe without requiring explicit save/load calls from users.
- **`NetworkXGraph` secondary indexes** — Added a PK index for O(1)-style identity lookup and a property index for exact-match searches, with new query helpers (`find_nodes_by_property`, `find_nodes`) and persisted index state.
- **`NetworkXGraph` optional vector indexes** — Added user-triggered ANN indexing for vector properties via `hnswlib`, including `enable_vector_index(...)` and `query_vector_index(...)`, with automatic synchronization on node mutations and persisted vector index files.
- **`GraphStore` vector API** — Added package-wide vector-index interface methods (`enable_vector_index`, `query_vector_index`) so vector capabilities are exposed consistently across backends.
- **Tutorial notebooks** — Added a new tutorials section with introductory and backend-specific notebooks under `docs/tutorials/`.

### Changed

- **`MockGraph` → `NetworkXGraph`** — Class and module renamed throughout the codebase to reflect the actual backend implementation. Affected files: `drm/networkx_graph.py`, `drm/__init__.py`, `test/test_drm.py`, `test/visualize_graph.py`, `test/visualize_mock_graph.py`.
- **`Neo4jGraph` inherits from `GraphStore`** — Now implements the `GraphStore` ABC interface.
- **`drm/entities.py` → `drm/drm_entities.py`** — Module renamed to follow the project convention (e.g., `neo4j_graph.py`, `networkx_graph.py`).
- **Entity hierarchy refactored** — Introduced base classes to reduce duplication:
  - `Individu` → `IndividuPadro`, `IndividuFoto`
  - `Lloc` → `LlocPadro`, `LlocFoto`
  - `DocumentCultural` (Node) → `Fons`, `ActaTemporal`
  - `Layout` (WeakNode) → `RegioFisica`, `OCRTranscript`
  - `_DocumentCulturalBase` (WeakNode) → `Padro`, `Fotografia`, `BOE`
- **`WeakNode` calls in tests** — All `WeakNode(parent, ...)` positional calls updated to `WeakNode(parent=parent, ...)` keyword syntax.
- **`test_node_pk_none_without_neo4j_id`** — Updated to verify that `pk=None` creates a valid node with `_primary_key = None` (was previously expecting `ValueError`).
- **Neo4j real test configuration** — `test/test_neo4j_real.py`, `test/test_graph_store_contract.py`, and `test/test_create_graph.py` now support target-based environment variables via `NEO4J_TARGET` and default to the `DEV` target when no explicit target is set, with backward-compatible fallback to plain `NEO4J_*` vars.

### Fixed

- **`IndividuFoto.be_value_properties`** — Added missing `be_value_properties = ()` attribute that caused `AttributeError` on instantiation.
- **`Esdeventiment` duplicate `pk` kwarg** — Fixed `TypeError` caused by passing `pk` both explicitly and via `**kwargs`.
- **`IndividuPadro.ignore_assertion` test** — Added missing `pk=1` argument.
- **`WeakNode` parent validation** — Nodes with `pk=None` (transient) cannot be parents of `WeakNode`; raises `ValueError`.
- **`__repr__` for nodes with `_primary_key = None`** — No longer crashes.
- **`version` setter** — Skips `_single_pk` transformation when `_primary_key` is `None`.
- **`__setitem__` with `key="attributes"`** — Uses `pop(..., None)` instead of `pop(...)` to handle missing `_primary_key`.

### Documentation

- **README.md** — Updated with `NetworkXGraph` name, correct `WeakNode(parent=...)` syntax, new **Primary Key** section with rules table and examples.
- **docs/index.rst** — Updated with `NetworkXGraph` name, entity hierarchy description, and **Primary Key** section.
- **docs/api/drm_entities.rst** — Renamed from `entities.rst`.
- **Notebook dependencies** — Added `notebook`, `ipykernel`, and `ipywidgets` to project environments.
- **Interactive WeakNode tutorial** — Added `docs/tutorials/notebooks/04_networkx_weaknodes_interactive.ipynb` with step-by-step state inspection and interactive add/delete controls.
