# 🚀 Quick Start Guide: Neo4j DEV Configuration

## Default DEV Credentials

```
Host:     localhost
Port:     7687 (bolt protocol)
User:     neo4j
Password: neo4j2026
Database: neo4j
```

## Setup Steps

### 1. Copy Configuration Template
```bash
cp .env.example .env
```

### 2. Verify .env Contents
```bash
cat .env | grep NEO4J_DEV
# Should show:
# NEO4J_DEV_URL=bolt://localhost:7687
# NEO4J_DEV_USER=neo4j
# NEO4J_DEV_PASSWORD=neo4j2026
# NEO4J_DEV_DATABASE=neo4j
```

### 3. Verify Neo4j is Running
```bash
# Check if Neo4j is accessible
nc -zv localhost 7687
# Expected: Connection succeeded

# Or test the connection:
python -c "
from neo4j import GraphDatabase
try:
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'neo4j2026'))
    print('✅ Connection successful!')
    driver.close()
except Exception as e:
    print(f'❌ Connection failed: {e}')
"
```

### 4. Run Tests
```bash
# Single test file
python -m pytest test/test_neo4j_real.py -v

# Expected output:
# test_update_node_pk_compost PASSED
# test_update_node_lloc_padro PASSED
# test_insert_individu_padro PASSED
# ... 11 passed ✅
```

---

## Troubleshooting

### Tests are SKIPPED
```
SKIPPED [Neo4j env config not found]
```
**Solution:** Verify `.env` exists and contains DEV config
```bash
ls -la .env
cat .env | grep NEO4J_DEV
```

### Connection Refused
```
ConnectionError: [Errno 111] Connection refused
```
**Solution:** Verify Neo4j is running on port 7687
```bash
# Check if Neo4j is running
ps aux | grep neo4j

# Or restart Neo4j
docker restart neo4j  # if using Docker
# or
neo4j start  # if using standalone
```

### Authentication Failed
```
AuthError: [SECURITY] Invalid username or password
```
**Solution:** Verify credentials in `.env`
```bash
# Expected:
NEO4J_DEV_USER=neo4j
NEO4J_DEV_PASSWORD=neo4j2026
```

---

## Manual Test (Without Pytest)

```python
import os
os.environ['NEO4J_DEV_URL'] = 'bolt://localhost:7687'
os.environ['NEO4J_DEV_USER'] = 'neo4j'
os.environ['NEO4J_DEV_PASSWORD'] = 'neo4j2026'

from test.test_neo4j_real import Neo4jRealTest
import unittest

# Run a single test
suite = unittest.TestLoader().loadTestsFromName(
    'test_update_node_pk_compost',
    Neo4jRealTest
)
unittest.TextTestRunner(verbosity=2).run(suite)
```

---

## Environment Variables Reference

| Variable | Value | Description |
|----------|-------|-------------|
| `NEO4J_DEV_URL` | `bolt://localhost:7687` | Connection URL |
| `NEO4J_DEV_USER` | `neo4j` | Username |
| `NEO4J_DEV_PASSWORD` | `neo4j2026` | Password |
| `NEO4J_DEV_DATABASE` | `neo4j` | Database name |
| `NEO4J_TARGET` | `DEV` | Active target (defaults to DEV) |

---

## Alternative Targets (Optional)

You can define multiple environments in `.env`:

```bash
# For PRODUCTION
NEO4J_TARGET=PROD
NEO4J_PROD_URL=bolt://prod-server:7687
NEO4J_PROD_USER=neo4j_prod
NEO4J_PROD_PASSWORD=your_prod_password

# For LOCAL development
NEO4J_TARGET=LOCAL
NEO4J_LOCAL_URL=bolt://localhost:7687
NEO4J_LOCAL_USER=neo4j
NEO4J_LOCAL_PASSWORD=neo4j
```

Then set the target:
```bash
# Switch to production
export NEO4J_TARGET=PROD
pytest test/test_neo4j_real.py -v

# Switch back to dev
export NEO4J_TARGET=DEV
# or just unset to use default DEV
unset NEO4J_TARGET
```

---

## Running All Tests

```bash
# Run in-memory tests (always pass, no Neo4j needed)
python -m pytest test/test_drm.py -v
# ✅ 112 passed

# Run contract tests (always pass, no Neo4j needed)
python -m pytest test/test_graph_store_contract.py -v
# ✅ 23 passed

# Run Neo4j tests (requires DEV connection)
python -m pytest test/test_neo4j_real.py -v
# ✅ 11 passed (with Neo4j) or 11 skipped (without)

# Run everything
python -m pytest test/ -v
```

---

**Last Updated:** 2026-07-11  
**Status:** ✅ Ready for Development

