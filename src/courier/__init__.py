from config import Config
from route import Route
from env.node import Node
from networkx import Graph
from dispatch import Order

import networkx as nx
from collections import defaultdict
from typing import Dict, Union, List

class Courier:

    orders: List[Order]
    route: Route

    def __init__(self, location, subgraph:Graph, config=None):

        if config is None:
            config = Config()
        self.config = config

        self.orders = []
        self.route = None
        self.initial_location = location

        self.subgraph = subgraph


    def get_state(self, time, next_node:Node=None) -> Dict[str, Union[float, Node]]:
        state = {'orders': [order for order in self.orders if not order.completed]}
        if self.route is None:
            if next_node is None:
                raise ValueError(f'next_node is not provided and the courier has not been assigned a node')
            if not self.subgraph.has_node(next_node):
                raise ValueError(f"next_node is not in the courier's proximity")
            state['next_node'] = next_node
            state['next_node_arrival_time'] = time \
                + nx.get_edge_attributes(self.subgraph,'travel_time')[('courier', next_node.name)]
        else:
            tmp = self.route.get_next_node()
            state['next_node'] = tmp['node']
            state['next_node_arrival_time'] = tmp['time']
            if tmp['node']!=next_node and next_node is not None:
                raise ValueError(f"next_node={next_node.name} is not the \
                                 next node in the courier's route ({tmp['node'].name})")

        return state
    
    def __setattr__(self, __name: str, __value):
        if __name != 'route':
            object.__setattr__(self, __name, __value)
        else:
            self.assign_route(__value)
    
    def assign_route(self, route:Route):
        if self.route is None:
            # TODO: implement some check here to make sure an invalid route is not
            #       being assigned
            self.route = route
        elif self.route.courier_state != route.courier_state:
            raise ValueError(f'Route cannot be assigned to courier due to differing next node states:\
                              {self.route.courier_state}!={route.courier_state}')
