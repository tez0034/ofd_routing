import networkx as nx
from config import Config

class Node:

    def __init__(self, graph, name, config = None, **kwargs):

        if config is None:
            config = Config()
        self.config = config

        self.graph = graph
        self.name = name

        # add graph to node if node does not exist
        if not self.graph.has_node(name):
            self.graph.add_node(name, **kwargs)
        else:
            nx.set_node_attributes(self.graph, {self.name:kwargs})

        self.subgraph = self.graph[name]
    
    def __getattr__(self, attr):
        try:
            return nx.get_node_attributes(self.graph, attr)[self.name]
        except:
            raise ValueError(f'Node {self.name} does not have attribute {attr}')
    
    def set_node_attribute_in_graph(self, attr_name, attr_value):
        nx.set_node_attributes(self.graph, {self.name:{attr_name:attr_value}})

    def get_edge_attributes(self, node, attr):
        return nx.get_edge_attributes(self.graph, attr)[(self.name, node.name)]