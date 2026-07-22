"""Tests unitaris per la classe Node.

Verifiquen el comportament intern del Node: pk_attributes, main_label,
labels, pk compostes i WeakNode.

Usage:
    python -m pytest test/test_node.py -v
"""

import unittest

from cvcdocdb.base import Node


class NodeTest(unittest.TestCase):
    def test_get_pk_attributes(self):
        r = Node(pk=0, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        s = Node(pk={'id': 0}, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        t = Node(pk={'code': 0}, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])

        self.assertEqual(
            [r['pk_attributes'], s['pk_attributes'], t['pk_attributes']],
            [{'id': 0}, {'id': 0}, {'code': 0}]
        )

    def test_set_pk_attributes(self):
        r = Node(pk=0, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        s = Node(pk={'id': 0}, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        t = Node(pk={'code': 0}, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])

        r['pk_attributes']['id'] = 1
        s['pk_attributes']['id'] = 1
        t['pk_attributes']['code'] = 1

        self.assertEqual(
            [r['pk_attributes'], s['pk_attributes'], t['pk_attributes']],
            [{'id': 1}, {'id': 1}, {'code': 1}]
        )

    def test_get_main_label(self):
        r = Node(pk=0, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        self.assertEqual([r['main_label'], r['labels']], ['test', ['test']])

    def test_set_main_label(self):
        r = Node(pk=0, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        r['main_label'] = 'test_2'
        self.assertEqual([r['main_label'], r['labels']], ['test_2', ['test_2']])

    def test_get_pk(self):
        r = Node(pk=0, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        s = Node(pk={'id': 0}, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        t = Node(pk={'code': 0}, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])

        self.assertEqual(
            [r['pk'], s['pk'], t['pk']],
            [
                {'main_label': 'test', 'pk': {'id': 0}},
                {'main_label': 'test', 'pk': {'id': 0}},
                {'main_label': 'test', 'pk': {'code': 0}},
            ]
        )

    def test_set_pk(self):
        r = Node(pk=0, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        s = Node(pk={'id': 0}, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        t = Node(pk={'code': 0}, main_label='test', type='text',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])

        r['pk_attributes']['id'] = 1
        s['pk_attributes']['id'] = 1
        t['pk_attributes']['code'] = 1

        self.assertEqual(
            [r['pk'], s['pk'], t['pk']],
            [
                {'main_label': 'test', 'pk': {'id': 1}},
                {'main_label': 'test', 'pk': {'id': 1}},
                {'main_label': 'test', 'pk': {'code': 1}},
            ]
        )

    def test_weak_node(self):
        s = Node(pk={'id': 0}, main_label='strong',
                 boundingbox=[0, 0, 1, 0, 1, 1, 1, 0])
        t = Node(pk={'code': 1}, main_label='weak', parent=s)
        v = Node(pk={'id': 2}, main_label='weak', parent=t)

        self.assertEqual(
            [s['parent'], t['parent'], s['pk'], t['pk'], v['pk']],
            [
                None, s,
                {'main_label': 'strong', 'pk': {'id': 0}},
                {'main_label': 'weak', 'pk': {'id': 0, 'code': 1}},
                {'main_label': 'weak', 'pk': {'id': 0, 'code': 1, 'id_0': 2}},
            ]
        )


if __name__ == '__main__':
    unittest.main()
