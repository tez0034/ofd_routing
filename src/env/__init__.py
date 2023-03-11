from env.node import Node
from config import Config
import networkx as nx
import numpy as np


class Environment:

    def __init__(self, env_graph = None, format = None, config = None):

        '''
        Arguments:
        env_graph (dict) -- {'nodes': [{'location:' node1_loc,'type': node1_type, ...}, 
                                       {'location:' node2_loc,'type': node2_type, ...}, 
                                       ...]
                             'edges': [(node1_1, node1_2, {'travel_time': t_1, ...}),
                                       (node2_1, node2_2, {'travel_time': t_2, ...}),
                                       ...]}
                             (if format = None, env_graph is assumed to be in the default format 
                             above; node and edges can have more attributes beyond those listed
                             above.)
        '''
        
        if config is None:
            config = Config()
        self.config = config
        
        if format == 'random':
            self.env_graph = self.random_init()
        elif format is None:
            self.env_graph = env_graph

    
    def process_env_graph(self):
        self.nodes = self.env_graph['nodes']
        self.node_locations = np.array([list(node['location']) for node in self.nodes])
        self.edges = self.env_graph['edges']
        self.graph = nx.Graph()
        self.graph.add_nodes_from([(i, node) for i,node in enumerate(self.nodes)])
        self.graph.add_edges_from(self.edges)
        

    def random_init(self):
        pass

    def get_travel_time(self, location1, location2):
        if self.config.travel_time_method == 'location':
            dist = (np.array(location1 - location2)**2).sum(-1).sqrt()
            time = dist/self.config.vehicle_speed
            time = np.maximum(time + np.random.normal(size=dist.shape)*self.config.travel_time_std_dev, 0) \
                    + self.config.min_travel_time
        else:
            raise Exception(f'Config option "travel_time_method" = {self.config.travel_time_method} is invalid')

    def get_nodes_near_location(self, location, max_distance):
        dist = (np.array(location[np.newaxis,:] - self.node_locations)**2).sum(-1).sqrt()
        valid_nodes = np.nonzero(dist < max_distance)[0]
        return valid_nodes
    
    def extract_subgraph_in_proximity(self, location, max_distance=5000, 
                                      name = 'vehicle', insert_node = True):
        valid_nodes = self.get_nodes_near_location(location, max_distance=max_distance)
        subgraph = self.graph.subgraph(valid_nodes).copy()
        subgraph.add_node(name)
        travel_time = self.get_travel_time(location, self.node_locations[valid_nodes,:])
        subgraph.add_edges([(name, node, tt) for node, tt in zip(valid_nodes, travel_time)])
        return subgraph