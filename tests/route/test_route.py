import unittest
import os
import sys
import numpy as np
import networkx as nx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from env import Environment
from route import Route

class TestRoute(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env_graph = {'nodes': [(0, {'location': [0,0],'type': 'store'}), 
                                   (1, {'location': [1,1],'type': 'customer'}),
                                   (2, {'location': [2,2],'type': 'store'}),
                                   (3, {'location': [3,3],'type': 'customer'})],
                         'edges': [(0, 1, {'travel_time': 1}),
                                   (1, 2, {'travel_time': 2}),
                                   (2, 3, {'travel_time': 3}),
                                   (0, 2, {'travel_time': 3}),
                                   (0, 3, {'travel_time': 6}),
                                   (1, 3, {'travel_time': 5})]}
        cls.en = Environment(env_graph=cls.env_graph)

    def test_invalid(self):
        courier_state = {'next_node_arrival_time': 100, 'orders':[], 'next_node': None}
        with self.assertWarns(Warning):
            rt = Route(node_sequence=[self.en.nodes[0], self.en.nodes[1], self.en.nodes[2]], 
                    courier_state = courier_state)
        self.assertFalse(rt.valid)
        rt_details = rt.route_details
        self.assertEqual(rt.route_details[0], {'node': self.en.nodes[0], 
                                               'time': courier_state['next_node_arrival_time']})
        self.assertEqual(rt.route_details[1], {'node': self.en.nodes[1], 
                                               'time': courier_state['next_node_arrival_time'] 
                                                        + 1 + self.en.config.store_wait_time})
        self.assertEqual(rt.route_details[2], {'node': self.en.nodes[2], 
                                               'time':  rt_details[1]['time'] + 2})
        self.assertEqual(rt.get_next_node(103), rt.route_details[1])
        self.assertEqual(rt.get_next_node(106), rt.route_details[2])
        