import unittest

from dlm.xpp_graph import XPPGraph
from dlm.entities import *
from dlm.base import *
import json


class XPPGraphTest(unittest.TestCase):
    def test_update_node_pk_compost(self, file="config.json"):
        "Test per validar la creacio de nodes"
        # Primer creo node
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

        with open(file) as f:
            data = json.load(f)
            Connection = XPPGraph(**data)

        up_a_1 = Connection.insertNode(a, replace=True)
        up_b_1 = Connection.insertNode(b, replace=False, update=True)

        Connection.close()
        self.assertEqual([up_a_1 >= 0, up_b_1 >= 0], [True, True])

    def test_update_node_Municipi(self, file="config.json"):
        "Test per validar la creacio de nodes"
        # Primer creo node
        a = LlocPadro(pk={"nom": "Caldes dEstrac", "any": 1905}, alternative_labels=["TEST"],estat="inserit")
        b = LlocPadro(
            pk={"nom": "Caldes dEstrac", "any": 1905},
            main_label="LlocPadro",
            alternative_labels=["TEST"],
            estat="actualitzat",
        )

        with open(file) as f:
            data = json.load(f)
            Connection = XPPGraph(**data)

        up_a_1 = Connection.insertNode(a, replace=True)
        up_b_1 = Connection.insertNode(b, replace=False, update=True)

        Connection.close()
        self.assertEqual([up_a_1 >= 0, up_b_1 >= 0], [True, True])

    def test_insert_individu(self, file="config.json"):
        "Test per validar la creacio de nodes"
        # Primer creo node

        ind_1 = {"nom": "Oriol", "cognom1": "Ramos", "edat": 18}
        ind_2 = {"nom": "Sergio", "cognom1": "Ramos", "ofici": "fuster"}
        ind_3 = {"nom": "Pere", "cognom1": "Fuster", "edat": "50"}
        a = IndividuPadro(**ind_1, alternative_labels="TEST")
        b = IndividuPadro(**ind_2, alternative_labels="TEST")
        c = IndividuPadro(**ind_3, alternative_labels="TEST")

        with open(file) as f:
            data = json.load(f)
            Connection = XPPGraph(**data)

        up_a = Connection.insertNode(a, replace=True)
        up_b = Connection.insertNode(b, replace=False, update=True)
        up_c = Connection.insertNode(c, replace=False, update=False)

        Connection.close()
        self.assertEqual([up_a >= 0, up_b >= 0, up_c >= 0], [True, True, True])


if __name__ == "__main__":
    unittest.main()
