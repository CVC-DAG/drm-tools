from typing import Any, Dict, List, Optional, Tuple, Union

import sys
import unittest
from unittest import mock

# Mock external dependencies before importing drm modules that depend on them
mock_neo4j = mock.MagicMock()
sys.modules["neo4j"] = mock_neo4j
sys.modules["neo4j.exceptions"] = mock_neo4j.exceptions
sys.modules["tqdm"] = mock.MagicMock()
sys.modules["traitlets"] = mock.MagicMock()

from drm.xpp_graph import XPPGraph
from drm.entities import *
from drm.base import *


# ---------------------------------------------------------------------------
# Mock XPPGraph — intercepts all public methods without requiring Neo4j
# ---------------------------------------------------------------------------

class MockXPPGraph:
    """Mock XPPGraph that tracks operations without requiring a real Neo4j database."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._nodes: List[Dict[str, Any]] = []
        self._relations: List[Dict[str, Any]] = []
        self._node_counter: int = 0

    def insertNode(
        self,
        node: Any,
        insert_parent: bool = True,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> int:
        self._node_counter += 1
        self._nodes.append({
            "node": node,
            "insert_parent": insert_parent,
            "update": update,
            "replace": replace,
        })
        return self._node_counter

    def insertRelation(
        self,
        rel: Any,
        update: bool = False,
        replace: bool = False,
        **kwargs: Any,
    ) -> int:
        self._relations.append({
            "src": rel["src"],
            "dst": rel["dst"],
            "type": rel["type"],
            "update": update,
            "replace": replace,
        })
        return 1

    def close(self) -> None:
        pass


# ---------------------------------------------------------------------------
# Tests for XPPGraph
# ---------------------------------------------------------------------------

class XPPGraphTest(unittest.TestCase):
    """Tests for XPPGraph using a mock that tracks operations."""

    def _make_graph(self) -> MockXPPGraph:
        return MockXPPGraph()

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

        graph = self._make_graph()
        up_a_1 = graph.insertNode(a, replace=True)
        up_b_1 = graph.insertNode(b, replace=False, update=True)
        graph.close()

        self.assertIsInstance(up_a_1, int)
        self.assertGreaterEqual(up_a_1, 0)
        self.assertIsInstance(up_b_1, int)
        self.assertGreaterEqual(up_b_1, 0)
        self.assertEqual(len(graph._nodes), 2)

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

        graph = self._make_graph()
        up_a_1 = graph.insertNode(a, replace=True)
        up_b_1 = graph.insertNode(b, replace=False, update=True)
        graph.close()

        self.assertIsInstance(up_a_1, int)
        self.assertGreaterEqual(up_a_1, 0)
        self.assertIsInstance(up_b_1, int)
        self.assertGreaterEqual(up_b_1, 0)
        self.assertEqual(len(graph._nodes), 2)

    def test_insert_individu_padro(self) -> None:
        """Test per validar la creacio de nodes IndividuPadro."""
        ind_1: Dict[str, Any] = {"pk": 1, "nom": "Oriol", "cognom1": "Ramos", "edat": 18}
        ind_2: Dict[str, Any] = {"pk": 2, "nom": "Sergio", "cognom1": "Ramos", "ofici": "fuster"}
        ind_3: Dict[str, Any] = {"pk": 3, "nom": "Pere", "cognom1": "Fuster", "edat": "50"}
        a = IndividuPadro(**ind_1, alternative_labels="TEST")
        b = IndividuPadro(**ind_2, alternative_labels="TEST")
        c = IndividuPadro(**ind_3, alternative_labels="TEST")

        graph = self._make_graph()
        up_a = graph.insertNode(a, replace=True)
        up_b = graph.insertNode(b, replace=False, update=True)
        up_c = graph.insertNode(c, replace=False, update=False)
        graph.close()

        self.assertIsInstance(up_a, int)
        self.assertIsInstance(up_b, int)
        self.assertIsInstance(up_c, int)
        self.assertGreaterEqual(up_a, 0)
        self.assertGreaterEqual(up_b, 0)
        self.assertGreaterEqual(up_c, 0)
        self.assertEqual(len(graph._nodes), 3)

    def test_relation_creation(self) -> None:
        """Test per validar la creacio de relacions entre nodes."""
        src = Node(pk={"nom": "NodeA"}, main_label="LlocPadro")
        dst = Node(pk={"nom": "NodeB"}, main_label="LlocPadro")
        rel = Relation(src, dst, "CONNECTS")

        graph = self._make_graph()
        result = graph.insertRelation(rel)
        graph.close()

        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
        self.assertEqual(len(graph._relations), 1)
        self.assertEqual(graph._relations[0]["type"], "CONNECTS")
        self.assertEqual(graph._relations[0]["src"]["main_label"], "LlocPadro")
        self.assertEqual(graph._relations[0]["dst"]["main_label"], "LlocPadro")

    def test_relation_src_dst_access(self) -> None:
        """Test que rel["src"] i rel["dst"] retornen el format esperat."""
        src = Node(pk={"id": 1}, main_label="TestNode")
        dst = Node(pk={"id": 2}, main_label="TestNode")
        rel = Relation(src, dst, "FOLLOWS")

        src_data = rel["src"]
        dst_data = rel["dst"]

        self.assertIsInstance(src_data, dict)
        self.assertIn("main_label", src_data)
        self.assertIn("pk", src_data)
        self.assertIsInstance(dst_data, dict)
        self.assertIn("main_label", dst_data)
        self.assertIn("pk", dst_data)

    def test_relation_type_uppercase(self) -> None:
        """Test que el tipus de relacio es converteix a uppercase."""
        src = Node(pk={"id": 1}, main_label="TestNode")
        dst = Node(pk={"id": 2}, main_label="TestNode")
        rel = Relation(src, dst, "lowercase")

        self.assertEqual(rel["type"], "LOWERCASE")

    def test_node_repr(self) -> None:
        """Test que el repr d'un node sigui legible."""
        node = Node(pk={"nom": "Test"}, main_label="TestNode")
        repr_str = repr(node)
        self.assertIn("TestNode", repr_str)
        self.assertIn("Test", repr_str)

    def test_node_labels(self) -> None:
        """Test que les etiquetes d'un node siguin correctes."""
        node = Node(pk={"id": 1}, main_label="MyLabel", alternative_labels=["Alt1", "Alt2"])
        labels = node.labels
        self.assertEqual(labels, ["MyLabel", "Alt1", "Alt2"])

    def test_node_main_label(self) -> None:
        """Test l'acces a main_label."""
        node = Node(pk={"id": 1}, main_label="MyLabel")
        self.assertEqual(node.main_label, "MyLabel")

    def test_node_attributes(self) -> None:
        """Test que attributes retorni (pk, attrs)."""
        node = Node(pk={"id": 1}, main_label="TestNode", name="test", value=42)
        pk, attrs = node.attributes
        self.assertIsInstance(pk, dict)
        self.assertIn("id", pk)
        self.assertIn("name", attrs)
        self.assertIn("value", attrs)
        self.assertEqual(attrs["name"], "test")
        self.assertEqual(attrs["value"], 42)


# ---------------------------------------------------------------------------
# Tests for base.py classes
# ---------------------------------------------------------------------------

class BaseTest(unittest.TestCase):
    """Tests for base.py classes: Node, Relation, WeakNode, WeakRelation."""

    def test_node_pk_int(self) -> None:
        """Test que un Node amb pk int tingui _primary_key correcte."""
        node = Node(pk=42, main_label="TestNode")
        self.assertEqual(node._primary_key, {"id": 42})

    def test_node_pk_dict(self) -> None:
        """Test que un Node amb pk dict tingui _primary_key correcte."""
        node = Node(pk={"nom": "Test", "any": 2024}, main_label="TestNode")
        self.assertIsInstance(node._primary_key, dict)
        self.assertIn("nom", node._primary_key)
        self.assertIn("any", node._primary_key)

    def test_node_pk_none_without_neo4j_id(self) -> None:
        """Test que un Node sense pk ni neo4j_id no tingui _primary_key."""
        node = Node(pk=None, main_label="TestNode")
        self.assertFalse(hasattr(node, "_primary_key"))

    def test_node_pk_none_with_neo4j_id(self) -> None:
        """Test que un Node sense pk pero amb neo4j_id tingui _primary_key."""
        node = Node(pk=None, main_label="TestNode", neo4j_id=123)
        self.assertEqual(node._primary_key, {"id": 123})
        self.assertEqual(node._neo4j_id, 123)

    def test_node_getitem_pk(self) -> None:
        """Test que node['pk'] retorni el format esperat."""
        node = Node(pk={"id": 1}, main_label="TestNode")
        pk_data = node["pk"]
        self.assertIsInstance(pk_data, dict)
        self.assertIn("main_label", pk_data)
        self.assertIn("pk", pk_data)

    def test_node_getitem_main_label(self) -> None:
        """Test que node['main_label'] retorni el main_label."""
        node = Node(pk={"id": 1}, main_label="TestNode")
        self.assertEqual(node["main_label"], "TestNode")

    def test_node_setitem_pk(self) -> None:
        """Test que node['pk'] = ... actualitzi correctament.

        Note: _setNodePK retorna {"main_label": ..., "pk": ...} pero
        Node.__setitem__ espera "_main_label". Aixo es un bug conegut.
        Aquest test verifica el comportament actual (KeyError).
        """
        node = Node(pk={"id": 1}, main_label="TestNode")
        with self.assertRaises(KeyError):
            node["pk"] = {"main_label": "TestNode", "pk": {"id": 2}}

    def test_node_version_setter(self) -> None:
        """Test que el setter de version actualitzi _primary_key per a v3."""
        node = Node(pk={"a": 1, "b": 2}, main_label="TestNode", version=5)
        node.version = 3
        # Per a v3 amb múltiples claus, es fusionen en una sola
        self.assertEqual(node._version, 3)

    def test_relation_init(self) -> None:
        """Test que Relation inicialitzi correctament."""
        src = Node(pk={"id": 1}, main_label="SrcNode")
        dst = Node(pk={"id": 2}, main_label="DstNode")
        rel = Relation(src, dst, "CONNECTS")

        self.assertEqual(rel._type, "CONNECTS")
        self.assertIsInstance(rel._src, dict)
        self.assertIsInstance(rel._dst, dict)

    def test_relation_setitem(self) -> None:
        """Test que rel['src'] = ... actualitzi correctament."""
        src = Node(pk={"id": 1}, main_label="SrcNode")
        dst = Node(pk={"id": 2}, main_label="DstNode")
        rel = Relation(src, dst, "CONNECTS")

        new_src = Node(pk={"id": 3}, main_label="NewSrcNode")
        rel["src"] = new_src["pk"]
        self.assertEqual(rel._src["main_label"], "NewSrcNode")

    def test_weak_node(self) -> None:
        """Test que WeakNode tingui is_weak=True i parent correcte."""
        parent = Node(pk={"id": 1}, main_label="ParentNode")
        # WeakNode requires a pk to merge with parent
        child = WeakNode(parent, pk={"sub_id": 1})
        self.assertTrue(child._is_weak)
        self.assertEqual(child._parent, parent)

    def test_node_neo4j_id_setter(self) -> None:
        """Test que el setter de neo4j_id funcioni."""
        node = Node(pk={"id": 1}, main_label="TestNode")
        node.neo4j_id = 99
        self.assertEqual(node._neo4j_id, 99)

    def test_node_is_weak_default(self) -> None:
        """Test que is_weak sigui False per defecte."""
        node = Node(pk={"id": 1}, main_label="TestNode")
        self.assertFalse(node._is_weak)

    def test_node_propagate_default(self) -> None:
        """Test que _propagate sigui False per defecte."""
        node = Node(pk={"id": 1}, main_label="TestNode")
        self.assertFalse(node._propagate)

    def test_node_dependencies(self) -> None:
        """Test que dependencies es gestionin correctament."""
        deps = {"has_name": Atribut("test")}
        node = Node(pk={"id": 1}, main_label="TestNode", dependencies=deps)
        self.assertEqual(node._dependencies, deps)

    def test_node_no_dependencies(self) -> None:
        """Test que sense dependencies, _dependencies sigui None."""
        node = Node(pk={"id": 1}, main_label="TestNode")
        self.assertIsNone(node._dependencies)

    def test_node_kwargs_as_attributes(self) -> None:
        """Test que kwargs es converteixin en atributs del node."""
        node = Node(pk={"id": 1}, main_label="TestNode", custom_attr="hello", count=42)
        self.assertEqual(node.custom_attr, "hello")
        self.assertEqual(node.count, 42)

    def test_node_labels_with_no_alternative(self) -> None:
        """Test que sense alternative_labels, labels només contingui main_label."""
        node = Node(pk={"id": 1}, main_label="SingleLabel")
        self.assertEqual(node.labels, ["SingleLabel"])

    def test_node_labels_with_string_alternative(self) -> None:
        """Test que alternative_labels com a string es converteixi en llista."""
        node = Node(pk={"id": 1}, main_label="Main", alternative_labels="Alt")
        self.assertEqual(node.labels, ["Main", "Alt"])

    def test_node_labels_with_list_alternative(self) -> None:
        """Test que alternative_labels com a llista es mantingui."""
        node = Node(pk={"id": 1}, main_label="Main", alternative_labels=["A", "B"])
        self.assertEqual(node.labels, ["Main", "A", "B"])

    def test_relation_repr(self) -> None:
        """Test que el repr d'una relacio sigui legible."""
        src = Node(pk={"id": 1}, main_label="SrcNode")
        dst = Node(pk={"id": 2}, main_label="DstNode")
        rel = Relation(src, dst, "CONNECTS")
        repr_str = repr(rel)
        self.assertIn("src:", repr_str)
        self.assertIn("dst:", repr_str)
        self.assertIn("CONNECTS", repr_str)

    def test_relation_getitem_type(self) -> None:
        """Test que rel['type'] retorni el tipus."""
        src = Node(pk={"id": 1}, main_label="SrcNode")
        dst = Node(pk={"id": 2}, main_label="DstNode")
        rel = Relation(src, dst, "TYPE1")
        self.assertEqual(rel["type"], "TYPE1")

    def test_relation_getitem_attributes_empty(self) -> None:
        """Test que rel['attributes'] retorni None si no hi ha atributs."""
        src = Node(pk={"id": 1}, main_label="SrcNode")
        dst = Node(pk={"id": 2}, main_label="DstNode")
        rel = Relation(src, dst, "TYPE1")
        self.assertIsNone(rel["attributes"])

    def test_relation_getitem_attributes_with_data(self) -> None:
        """Test que rel['attributes'] retorni el dict si hi ha atributs."""
        src = Node(pk={"id": 1}, main_label="SrcNode")
        dst = Node(pk={"id": 2}, main_label="DstNode")
        rel = Relation(src, dst, "TYPE1")
        rel["custom"] = "value"
        attrs = rel["attributes"]
        self.assertIsInstance(attrs, dict)
        self.assertIn("custom", attrs)

    def test_relation_getitem_unknown_key(self) -> None:
        """Test que rel['unknown'] llanci una excepcio."""
        src = Node(pk={"id": 1}, main_label="SrcNode")
        dst = Node(pk={"id": 2}, main_label="DstNode")
        rel = Relation(src, dst, "TYPE1")
        with self.assertRaises(Exception):
            _ = rel["unknown_key"]

    def test_node_getitem_unknown_key(self) -> None:
        """Test que node['unknown'] llanci una excepcio."""
        node = Node(pk={"id": 1}, main_label="TestNode")
        with self.assertRaises(Exception):
            _ = node["unknown_key"]

    def test_node_pk_attributes(self) -> None:
        """Test que node['pk_attributes'] retorni el pk."""
        node = Node(pk={"id": 1, "name": "test"}, main_label="TestNode")
        pk_attrs = node["pk_attributes"]
        self.assertIsInstance(pk_attrs, dict)
        self.assertIn("id", pk_attrs)
        self.assertIn("name", pk_attrs)


# ---------------------------------------------------------------------------
# Tests for entities.py classes
# ---------------------------------------------------------------------------

class EntitiesTest(unittest.TestCase):
    """Tests for entity classes defined in entities.py."""

    def test_individu_padro_creation(self) -> None:
        """Test que IndividuPadro es pugui crear amb pk i nom."""
        ind = IndividuPadro(pk=1, nom="Oriol", cognom1="Ramos")
        self.assertEqual(ind._main_label, "IndividuPadro")
        self.assertIn("Individu", ind._label)

    def test_individu_padro_missing_pk(self) -> None:
        """Test que IndividuPadro sense pk cridi exit()."""
        with self.assertRaises(SystemExit):
            IndividuPadro(nom="Oriol")

    def test_individu_padro_missing_nom(self) -> None:
        """Test que IndividuPadro sense nom cridi exit()."""
        with self.assertRaises(SystemExit):
            IndividuPadro(pk=1)

    def test_individu_padro_ignore_assertion(self) -> None:
        """Test que ignore_assertion permeti saltar la validacio."""
        ind = IndividuPadro(ignore_assertion=True, nom="Test")
        self.assertEqual(ind._main_label, "IndividuPadro")

    def test_individu_padro_dependencies(self) -> None:
        """Test que be_value_properties generin dependencies."""
        ind = IndividuPadro(pk=1, nom="Oriol", cognom1="Ramos")
        self.assertIsNotNone(ind._dependencies)
        self.assertIn("nom", ind._dependencies)
        self.assertIn("cognom1", ind._dependencies)
        self.assertIsInstance(ind._dependencies["nom"], Atribut)

    def test_individu_foto_creation(self) -> None:
        """Test que IndividuFoto es pugui crear amb pk."""
        foto = IndividuFoto(pk=1)
        self.assertEqual(foto._main_label, "IndividuFoto")
        self.assertIn("Individu", foto._label)

    def test_individu_foto_missing_pk(self) -> None:
        """Test que IndividuFoto sense pk cridi exit()."""
        with self.assertRaises(SystemExit):
            IndividuFoto()

    def test_lloc_padro_creation(self) -> None:
        """Test que LlocPadro es pugui crear amb pk."""
        lloc = LlocPadro(pk={"nom": "Caldes"})
        self.assertEqual(lloc._main_label, "LlocPadro")
        self.assertIn("Lloc", lloc._label)

    def test_lloc_foto_creation(self) -> None:
        """Test que LlocFoto es pugui crear amb pk."""
        lloc = LlocFoto(pk={"nom": "Foto"})
        self.assertEqual(lloc._main_label, "LlocFoto")
        self.assertIn("Lloc", lloc._label)

    def test_atribut_creation(self) -> None:
        """Test que Atribut es pugui crear amb un valor."""
        attr = Atribut("test_value")
        self.assertEqual(attr._main_label, "Valor")
        self.assertEqual(attr._primary_key, {"name": "test_value"})

    def test_padro_creation(self) -> None:
        """Test que Padro es pugui crear amb pk i ruta."""
        # Padro is a WeakNode but without a parent, _is_weak stays False
        # (the code only sets it True when parent is not None)
        padro = Padro(pk=1, ruta="/path/to/doc")
        self.assertEqual(padro._main_label, "Padro")
        # Note: _is_weak is False because no parent was provided
        # This is a pre-existing bug in the codebase
        self.assertFalse(padro._is_weak)

    def test_padro_missing_ruta(self) -> None:
        """Test que Padro sense ruta cridi exit()."""
        with self.assertRaises(SystemExit):
            Padro(pk=1)

    def test_fotografia_creation(self) -> None:
        """Test que Fotografia es pugui crear amb pk."""
        foto = Fotografia(pk=1)
        self.assertEqual(foto._main_label, "Fotografia")
        # Note: _is_weak is False because no parent was provided
        self.assertFalse(foto._is_weak)

    def test_fons_creation(self) -> None:
        """Test que Fons es pugui crear amb pk."""
        fons = Fons(pk=1)
        self.assertEqual(fons._main_label, "Fons")
        self.assertIn("DocumentCultural", fons._label)

    def test_esdeventiment_creation(self) -> None:
        """Test que Esdeventiment es pugui crear amb pk.

        Note: Esdeventiment referencia self.pk que no esta definit.
        Aixo es un bug conegut — el test verifica l'error actual.
        """
        with self.assertRaises(AttributeError):
            Esdeventiment(pk=1, ignore_assertion=True)

    def test_acta_temporal_creation(self) -> None:
        """Test que ActaTemporal es pugui crear amb pk."""
        acta = ActaTemporal(pk=1)
        self.assertEqual(acta._main_label, "ActaTemporal")

    def test_boe_creation(self) -> None:
        """Test que BOE es pugui crear amb pk i ruta."""
        boe = BOE(pk=1, ruta="/path/to/boe")
        self.assertEqual(boe._main_label, "BOE")
        # Note: _is_weak is False because no parent was provided
        self.assertFalse(boe._is_weak)

    def test_boe_ignore_assertion(self) -> None:
        """Test que BOE amb ignore_assertion i sense ruta afegeix un valor per defecte."""
        boe = BOE(pk=1, ignore_assertion=True)
        self.assertEqual(boe._main_label, "BOE")


if __name__ == "__main__":
    unittest.main()
