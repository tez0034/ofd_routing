from env.node import Node
from config import Config

class Store(Node):

    valid_attribute_names = Config.store_valid_attribute_names

    def __init__(self, graph, name, location):
        super().__init__(graph, name, location=location)

    def __setattr__(self, attr_name, attr_value):
        if attr_name not in self.valid_attribute_names:
            raise ValueError(f'Attribute name {attr_name} is invalid for Store object')
        return super().__setattr__(attr_name, attr_value)