from env.node import Node
from config import Config

class Customer(Node):

    valid_attribute_names = Config.customer_valid_attribute_names

    def __init__(self, graph, name, **kwargs):
        super().__init__(graph, name, **kwargs)
        self.orders = None
    
    def __setattr__(self, attr_name, attr_value):
        object.__setattr__(self, attr_name, attr_value)
        if attr_name in self.valid_attribute_names:
            self.set_node_attribute_in_graph(attr_name, attr_value)
        


    
