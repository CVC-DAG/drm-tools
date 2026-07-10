# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation
- Install in editable mode: `pip install -e .`

### Testing
- Run all tests: `python -m pytest test/ -v`
- Run a single test file: `python -m pytest test/<test_file_name>.py`

### Documentation
- Generate HTML documentation with Sphinx:
  `sphinx-build -b html docs/ docs/_build/html/`
  (Or use the virtual environment: `.venv/bin/sphinx-build -b html docs/ docs/_build/html/`)

## Architecture & Core Concepts

### Overview
This library implements a graph-based document representation model. It supports two backends: `Neo4jGraph` for persistent storage in Neo4j and `MockGraph` (using NetworkX) for lightweight in-memory testing.

### Core Data Models
- **Node**: The fundamental building block, consisting of a `main_label` and a `pk` (primary key).
- **WeakNode**: A node whose identity is tied to a parent. Its `pk` is a composite of the parent's `pk` and its own. This models hierarchical structures like *Document $\rightarrow$ Section $\rightarrow$ Page*.
- **Relation**: A typed edge connecting two nodes.
- **WeakRelation**: A relation between a parent and a `WeakNode` that carries a `_propagate=True` flag, enabling **cascade delete** (deleting the parent automatically deletes the child).

### Key Concepts
- **Semantic Entities**: Domain-specific node types (e.g., `IndividuPadro`, `LlocPadro`) defined within the graph.
- **Cascade Delete**: Enabled by `WeakNode` and `WeakRelation` via the `_propagate` flag.
- **Backends**:
    - `Neo4jGraph`: Full Neo4j integration.
    - `MockGraph`: In-memory implementation for testing.
