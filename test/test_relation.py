"""Tests unitaris per la classe Relation.

Verifiquen el comportament de src/dst dins les relacions i la
propagació de canvis als pk_attributes dels nodes.

Usage:
    python -m pytest test/test_relation.py -v
"""

import unittest

from cvcdocdb.base import Relation, Node


class RelationTest(unittest.TestCase):
    def test_get_node_pks(self):
        a = Node(pk=0, main_label='test_1', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        b = Node(pk={'id': 1}, main_label='test_2', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])

        r = Relation(a, b, 'test_r')

        self.assertEqual([r['src'], r['dst']],
                         [a['pk'], b['pk']])

    def test_set_node_pks_from_rel(self):
        a = Node(pk=0, main_label='test_1', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        b = Node(pk={'id': 1}, main_label='test_2', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])

        r = Relation(a, b, 'test_r')

        r['src']['pk']['id'] = 1
        r['dst']['pk']['id'] = 1

        self.assertEqual([r['src'], r['dst']],
                         [a['pk'], b['pk']])

    def test_set_node_pks_from_node(self):
        a = Node(pk=0, main_label='test_1', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        b = Node(pk={'id': 1}, main_label='test_2', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])

        r = Relation(a, b, 'test_r')

        a['pk_attributes']['id'] = 1
        b['pk_attributes']['id'] = 1

        self.assertEqual([r['src'], r['dst']],
                         [a['pk'], b['pk']])


if __name__ == '__main__':
    unittest.main()
