import networkx as nx

class Node:

    def __init__(self, graph, name, **kwargs):

        self.graph = graph

        # add graph to node if node does not exist
        if not graph.has_node():
            graph.add_node(name, **kwargs)
        else:
            nx.set_node_attributes(self.graph, {self.name:kwargs})

        self.subgraph = graph[name]
        self.name = name
    
    def __getattr__(self, attr):
        try:
            return nx.get_node_attributes(self.graph, attr)[self.name]
        except:
            raise ValueError(f'Node {self.name} does not have attribute {attr}')
    
    def __setattr__(self, attr_name, attr_value):
        nx.set_node_attributes(self.graph, {self.name:{attr_name:attr_value}})