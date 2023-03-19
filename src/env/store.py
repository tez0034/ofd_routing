from env.node import Node
from config import Config

class Store(Node):

    valid_attribute_names = Config.store_valid_attribute_names

    def __init__(self, graph, name, config=None, wait_time=None, **kwargs):

        if config is None:
            config = Config()

        if wait_time is None:
            wait_time = config.store_wait_time
        else:
            wait_time = wait_time

        super().__init__(graph, name, config=config, wait_time=wait_time, **kwargs)

    def __setattr__(self, attr_name, attr_value):
        object.__setattr__(self, attr_name, attr_value)
        if attr_name in self.valid_attribute_names:
            self.set_node_attribute_in_graph(attr_name, attr_value)
        