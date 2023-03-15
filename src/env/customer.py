from env.node import Node
from config import Config

class Customer(Node):

    valid_attribute_names = Config.customer_valid_attribute_names

    def __init__(self, graph, name, **kwargs):
        super().__init__(graph, name, **kwargs)
    
    def __setattr__(self, attr_name, attr_value):
        if attr_name not in self.valid_attribute_names:
            raise ValueError(f'Attribute name {attr_name} is invalid for Store object')
        return super().__setattr__(attr_name, attr_value)


    
