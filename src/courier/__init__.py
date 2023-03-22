from config import Config
from collections import defaultdict

class Courier:

    def __init__(self, config=None):

        if config is None:
            config = Config()
        self.config = config

        self.orders = []
        self.route = None

    def get_state(self, time):
        state = {}
        if self.route is None:
            state['next_node'] = None
            state['next_node_arrival_time'] = None
        else:
            tmp = self.route.get_next_node()
            state['next_node'] = tmp['node']
            state['next_node_arrival_time'] = tmp['time']
