# Tests

Three levels of tests, organized with pytest markers:

## Levels

| Level | Marker | Count | Time | Description |
|-------|--------|-------|------|-------------|
| **Unit** | `pytest -m unit` | 43 | ~2s | Fast, no graph store (Node, Relation, schema generation) |
| **Integration** | `pytest -m integration` | 215 | ~3s | NetworkXGraph tests (in-memory, no Neo4j required) |
| **Neo4j** | `pytest -m slow` | 44 | ~10s | Neo4j integration tests (require real Neo4j connection) |

## Usage

```bash
# Run all tests (302 tests, ~10s)
pytest test/ -v

# Run only unit tests (fast, ~2s)
pytest test/ -m unit

# Run NetworkX integration tests (~3s)
pytest test/ -m integration

# Skip Neo4j tests (CI without Neo4j)
pytest test/ -m "not slow"

# Run only Neo4j tests (requires NEO4J_DEV_* env vars)
pytest test/ -m slow
```

## Test files

### Unit (no graph store)
- `test_node.py` — Node class internals
- `test_relation.py` — Relation class internals
- `test_schema_gen.py` — YAML-to-Python class generation
- `test_rdf_schema.py` — RDF/OWL-to-YAML conversion

### NetworkX integration
- `test_drm.py` — Full NetworkXGraph workflow (115 tests)
- `test_nx_query_integration.py` — Query and filtering
- `test_query_method.py` — Property-based search
- `test_schema_generation.py` — Schema YAML generation
- `test_schema_weaknode.py` — WeakNode detection in schemas
- `test_schema_weak_relation.py` — WeakRelation inference
- `test_graph_store_contract.py::TestNetworkXGraph` — Contract tests (23 tests)

### Neo4j integration
- `test_create_graph.py` — Neo4j node/relation creation
- `test_neo4j_real.py` — Real Neo4j workflow tests
- `test_graph_store_contract.py::TestNeo4jGraph` — Contract tests (24 tests)

## CI

In CI environments without Neo4j, run:

```bash
pytest test/ -v -m "not slow"
```
