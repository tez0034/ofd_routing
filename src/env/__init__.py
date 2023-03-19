from env.node import Node
from env.store import Store
from env.customer import Customer
from config import Config
import networkx as nx
import numpy as np


class Environment:

    def __init__(self, env_graph = None, format = None, config = None):

        '''
        Arguments:
        env_graph (dict) -- {'nodes': [(node_1, {'location:' node1_loc,'type': node1_type, ...}), 
                                       (node_2, {'location:' node2_loc,'type': node2_type, ...}), 
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
        
        self.graph = self.process_env_graph(self.env_graph)
        self.nodes = {}
        self.update_nodes()

        self.node_locations = None
        self.idx_to_name = None
        self.refresh_locations()


    @staticmethod
    def process_env_graph(env_graph):
        nodes = env_graph['nodes']
        edges = env_graph['edges']
        graph = nx.Graph()
        graph.add_nodes_from([(name, node) for name,node in nodes])
        graph.add_edges_from(edges)
        return graph
    
    def refresh_locations(self):
        '''
        Update location array
        '''
        locations = nx.get_node_attributes(self.graph, 'location')
        self.idx_to_name = {i:name for i, name in enumerate(self.graph.nodes)}
        self.node_locations = np.array([list(locations[self.idx_to_name[i]]) 
                                        for i in range(self.graph.number_of_nodes())])
        

    def random_init(self, n_nodes = None):
        if n_nodes is None:
            n_nodes = self.config.random_init_n_nodes
        env_graph = {'nodes':[], 'edges':[]}
        location = np.random.uniform(size=[n_nodes, 2])
        location = location * np.array(self.config.map_size)[np.newaxis,:]
        travel_times = self.get_travel_time(location[np.newaxis,:,:], location[:, np.newaxis, :],
                                            vehicle_speed=self.config.vehicle_speed)
        n_stores = int(n_nodes*self.config.store_to_customer_ratio)
        for i, _ in enumerate(location):
            node_type = 'store' if i<n_stores else 'customer'
            env_graph['nodes'].append((i, {'location': location[i,:].flatten(), 'type': node_type}))
            for ii in range(i):
                env_graph['edges'].append((i, ii, {'travel_time': travel_times[i][ii]}))
        return env_graph


    def update_nodes(self):
        '''
        Init new nodes, delete old nodes from dict
        '''
        # Initialize new nodes and add to dict
        for node in set(self.graph.nodes) - set(self.nodes.keys()):
            if nx.get_node_attributes(self.graph, 'type')[node] == 'store':
                self.nodes[node] = Store(self.graph, node)
            elif nx.get_node_attributes(self.graph, 'type')[node] == 'customer':
                self.nodes[node] = Customer(self.graph, node)

        # Remove old nodes
        for node in set(self.nodes.keys()) - set(self.graph.nodes):
            self.nodes.pop(node)
        
    def get_travel_time(self, location1, location2, vehicle_speed):
        if self.config.travel_time_method == 'location':
            dist = (np.array(location1 - location2)**2).sum(-1)**0.5
            time = dist/vehicle_speed
            time = np.maximum(time + np.random.normal(size=dist.shape)*self.config.travel_time_std_dev, 0) \
                    + self.config.min_travel_time
            return time
        else:
            raise Exception(f'Config option "travel_time_method" = {self.config.travel_time_method} is invalid')

    def get_nodes_near_location(self, location, max_distance):
        dist = ((np.array(location)[np.newaxis,:] - self.node_locations)**2).sum(-1)**0.5
        valid_nodes = np.nonzero(dist < max_distance)[0]
        return valid_nodes
    
    def extract_subgraph_in_proximity(self, location, max_distance=5000, 
                                      name='vehicle', vehicle_speed=None, insert_node=True):
        if vehicle_speed is None:
            vehicle_speed = self.config.vehicle_speed
        valid_nodes = self.get_nodes_near_location(location, max_distance=max_distance)
        subgraph = self.graph.subgraph(valid_nodes).copy()
        if insert_node:
            subgraph.add_node(name)
            travel_time = self.get_travel_time(location, self.node_locations[valid_nodes,:], vehicle_speed)
            subgraph.add_edges_from([(name, node, {'travel_time':tt}) for node, tt in zip(valid_nodes, travel_time)])
        return subgraph