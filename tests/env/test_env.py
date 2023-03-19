import unittest
import os
import sys
import numpy as np
import networkx as nx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from env import Environment
from env.store import Store
from env.customer import Customer

class TestEnvironment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.en = Environment(format='random')

    def test_base(self):
        self.assertEqual(len(self.en.nodes), self.en.config.random_init_n_nodes)
        self.assertIn('nodes', self.en.env_graph)
        self.assertIn('edges', self.en.env_graph)

        node_0 = self.en.nodes[0]
        self.assertTrue(isinstance(node_0, Store))
        self.assertEqual(node_0.wait_time, self.en.config.store_wait_time)
        
        node_0.wait_time = 100
        self.assertEqual(nx.get_node_attributes(self.en.graph, 'wait_time')[node_0.name],100)