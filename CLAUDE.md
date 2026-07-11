# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Branch Strategy

**Always work on the `develop` branch unless explicitly told otherwise.**

- **`develop`** — Active development branch. All substantial changes, new features, refactors, and bug fixes go here.
- **`main`** — Release branch. Only minor changes for preparing releases (version bumps, changelog entries, doc links). Never add features or make structural changes here.

Before starting any work, check the current branch:
```bash
git branch --show-current
```
If on `main`, switch to `develop` first:
```bash
git checkout develop
```

## Development Commands

### Installation
- Install in editable mode: `pip install -e .`

### Testing
- Run all tests: `python -m pytest test/ -v`
- Run a single test file: `python -m pytest test/<test_file_name>.py`

### Documentation
- Generate HTML documentation with Sphinx:
  `sphinx-build -b html docs/ docs/_build/html/`
  (Or use the virtual environment: `.venv/bin de sphinx-build -b html docs/ docs/_build/html/`)

## Architecture & Core Concepts

### Overview
This library implements a graph-based document representation model. It supports two backends: `Neo4jGraph` for persistent storage in Neo4j and `NetworkXGraph` for lightweight in-memory testing.

### Core Data Models
- **Node**: The fundamental building block, consisting of a `main_label` and a `pk` (primary key).
- **WeakNode**: A node whose identity is tied to a parent. Its `pk` is a composite of the parent's `pk` and its own. This models hierarchical structures like *Document $\rightarrow$ Section $\rightarrow$ Page*.
- **Relation**: A typed edge connecting two nodes.
- **WeakRelation**: A relation between a parent and a `WeakNode` that carries a `_propagate=True` flag, enabling **cascade delete** (deleting the parent automatically deletes the child).

### IMPORTANT: Backend Integrity
- **DO NOT MODIFY** the core logic, functions, or internal implementation of the Neo4j backend (specifically files in `drm/` and `test/test_neo4j_real.py`) unless explicitly instructed to do so within a dedicated, isolated branch and for a specific, documented task.
- Any structural changes to the backend must follow a formal review process.

## Key Concepts
- **Semantic Entities**: Domain-specific node types (e.g., `IndividuPadro`, `LlocPadro`) defined within the graph.
- **Cascade Delete**: Enabled by `WeakNode` and `WeakRelation` via the `_propagate` flag.
- **Backends**:
    - `Neo4jGraph`: Full Neo4j integration.
    - `NetworkXGraph`: In-memory implementation for testing.
