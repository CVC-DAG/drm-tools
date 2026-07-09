"""Tests for Neo4jGraph — connect to a real Neo4j database.

These tests require a .env file in the project root with Neo4j
connection details (NEO4J_URL, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE).
They are skipped if the env vars are not set.

Usage:
    # Create .env in the project root:
    NEO4J_URL=bolt://localhost:7687
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=your_password
    NEO4J_DATABASE=neo4j

    # Run only the real Neo4j tests:
    python -m pytest test/test_neo4j_real.py -v
"""

import json
import os
import sys
import unittest

# Load .env from project root (parent of test/)
_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(_env_path):
    from dotenv import load_dotenv
    load_dotenv(_env_path)

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from drm.neo4j_graph import Neo4jGraph
from drm.entities import *
from drm.base import *


def _load_config() -> dict:
    """Load Neo4j connection config from .env environment variables.

    Returns None if required env vars are not set.
    """
    url = os.environ.get("NEO4J_URL")
    user = os.environ.get("NEO4J_USER")
    password = os.environ.get("NEO4J_PASSWORD")
    database = os.environ.get("NEO4J_DATABASE")

    if not url or not user or not password:
        return None

    return {
        "url": url,
        "user": user,
        "password": password,
        "database": database,
    }


def _skip_if_no_config() -> unittest.TestCase:
    """Return a skip decorator if config.json is missing."""
    config = _load_config()
    if config is None:
        return unittest.skip("config.json not found — skipping real Neo4j tests")
    return None


class Neo4jRealTest(unittest.TestCase):
    """Tests that connect to a real Neo4j database.

    These tests verify that Neo4jGraph works correctly with an actual
    Neo4j instance. They require a config.json file in the test directory.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.config = _load_config()
        if cls.config is None:
            raise unittest.SkipTest("config.json not found")
        cls.graph = Neo4jGraph(
            url=cls.config["url"],
            user=cls.config["user"],
            password=cls.config["password"],
            database=cls.config.get("database"),
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.graph.close()

    def test_update_node_pk_compost(self) -> None:
        """Test per validar la creacio de nodes amb pk compost."""
        a = Node(
            pk={"nom": "Caldes dEstrac", "any": 1905},
            main_label="LlocPadro",
            alternative_labels=["TEST"],
            estat="inserit",
        )
        b = Node(
            pk={"nom": "Caldes dEstrac", "any": 1905},
            main_label="LlocPadro",
            alternative_labels=["TEST"],
            estat="actualitzat",
        )

        up_a_1 = self.graph.insertNode(a, replace=True)
        up_b_1 = self.graph.insertNode(b, replace=False, update=True)

        self.assertGreaterEqual(up_a_1, 0)
        self.assertGreaterEqual(up_b_1, 0)

    def test_update_node_lloc_padro(self) -> None:
        """Test per validar la creacio de nodes LlocPadro."""
        a = LlocPadro(
            pk={"nom": "Caldes dEstrac", "any": 1905},
            alternative_labels=["TEST"],
            estat="inserit",
        )
        b = LlocPadro(
            pk={"nom": "Caldes dEstrac", "any": 1905},
            main_label="LlocPadro",
            alternative_labels=["TEST"],
            estat="actualitzat",
        )

        up_a_1 = self.graph.insertNode(a, replace=True)
        up_b_1 = self.graph.insertNode(b, replace=False, update=True)

        self.assertGreaterEqual(up_a_1, 0)
        self.assertGreaterEqual(up_b_1, 0)

    def test_insert_individu_padro(self) -> None:
        """Test per validar la creacio de nodes IndividuPadro."""
        ind_1: dict = {"nom": "Oriol", "cognom1": "Ramos", "edat": 18}
        ind_2: dict = {"nom": "Sergio", "cognom1": "Ramos", "ofici": "fuster"}
        ind_3: dict = {"nom": "Pere", "cognom1": "Fuster", "edat": "50"}
        a = IndividuPadro(**ind_1, alternative_labels="TEST")
        b = IndividuPadro(**ind_2, alternative_labels="TEST")
        c = IndividuPadro(**ind_3, alternative_labels="TEST")

        up_a = self.graph.insertNode(a, replace=True)
        up_b = self.graph.insertNode(b, replace=False, update=True)
        up_c = self.graph.insertNode(c, replace=False, update=False)

        self.assertGreaterEqual(up_a, 0)
        self.assertGreaterEqual(up_b, 0)
        self.assertGreaterEqual(up_c, 0)


if __name__ == "__main__":
    unittest.main()
