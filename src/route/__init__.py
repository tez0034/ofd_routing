from config import Config
from env.store import Store
from env.customer import Customer
from dispatch.order import Order

import warnings
from operator import itemgetter
from copy import deepcopy
from typing import List, Union

class Route:

    node_sequence: List[Union[Customer, Store]]
    orders: List[Order]

    def __init__(self, node_sequence, courier_state, config=None):

        '''
        node_sequence -- list: list of node references
        courier_state -- dict: state of courier at beginning of road
        '''

        if config is None:
            config = Config()
        self.config = config
        self.node_sequence = node_sequence
        self.courier_state = courier_state
        self.orders = courier_state['orders']

        self.process_route()

        self.valid = self.is_valid()
        if not self.valid:
            warnings.warn('Route is invalid, calculate_cost method is disabled')
        

    def process_route(self):
        orders_collected = [o.collected for o in self.orders]
        orders_completed = [None for o in self.orders]
        d = {'node': self.node_sequence[0],
             'arrival_time': self.courier_state['next_node_arrival_time'],
             'orders_collected': orders_collected,
             'orders_completed': orders_completed}

        self.route_details = []
        self.route_details.append(self.process_orders(d))
        for node in self.node_sequence[1:]:
            d = {'node': node,
                 'arrival_time': self.route_details[-1]['departure_time'] 
                                 + self.route_details[-1]['node'].get_edge_attributes(node, 'travel_time'),
                 'orders_collected': self.route_details[-1]['orders_collected'] ,
                 'orders_completed': self.route_details[-1]['orders_completed'] }
            self.route_details.append(self.process_orders(d))
        
    
    def process_orders(self, d):
        '''
        Arguments:
        d -- dict: {'node': Node instance,
                    'arrival_time': node arrival time,
                    'orders_collected': list of bool indicating if order has been collected,
                    'orders_completed': list of order completion times, None if not completed}
        '''
        if isinstance(d['node'], Store):
            ready_times = [(i,order.ready_time) for i, order in enumerate(self.orders) if order.store==d['node']]
            ready_times = [t for t in ready_times if t[1]>d['arrival_time']] # filter away already collected orders
            if ready_times:
                d['departure_time'] = max(d['arrival_time'], 
                                          min(d['arrival_time']+d['node'].wait_time, 
                                              max(ready_times,key=itemgetter[1])))
            else:
                d['departure_time'] = d['arrival_time']
            collected_orders = [t[0] for t in ready_times if t[1]< d['departure_time']]
            d['status_change'] = collected_orders
            for i in collected_orders:
                d['orders_collected'][i] = True
        elif isinstance(d['node'], Customer):
            completed_orders = [i for i,order in enumerate(self.orders) if 
                                order.customer==d['node'] and order.collected and (order.completed is None)]
            d['status_change'] = completed_orders
            for i in completed_orders:
                d['orders_completed'][i] = d['arrival_time']
            d['departure_time'] = d['arrival_time']
        return d


    def calculate_cost(self):
        cost = 0.
        for i, order in enumerate(self.orders):
            if self.route_details[-1]['order_completed'][i]:
                # validity check ensures that the customer's orders has been collected
                cost += order.calculate_cost(self.route_details[-1]['order_completed'][i])
            else:
                # append tentative order cost based on time at end of route since order has 
                # not yet been delivered
                cost += order.calculate_cost(self.route_details[-1]['arrival_time'])
        return cost
        

    def is_valid(self):
        if self.courier_state['next_node'] is not None and \
        self.node_sequence[0]!=self.courier_state['next_node']:
            # first node in route must be the courier's next destination
            return False
        for i, node in enumerate(self.node_sequence):
            if isinstance(node, Store):
                continue
            if isinstance(node, Customer):
                if (not any ([order.collected for order in node.orders])) and \
                    (len(set(self.node_sequence[:i]).intersection([order.store for order in node.orders]))==0):
                    # First condition: driver does not have any orders from customer initially
                    # Second condition: driver's route does not include stores from any of the customer's orders
                    return False
        return True
    
    def get_next_node(self, time):
        # note: if the time given is exactly the arrival time for a particular node, the
        # next node will be returned
        time_list = [d['arrival_time'] for d in self.route_details]
        idx = list(map(lambda i: i > time, time_list)).index(True) \
                if max(time_list)>time else (len(time_list)-1)
        return self.route_details[idx]
    
    def get_current_state(self, time):
        if time < self.route_details[0]['arrival_time']:
            return None
        elif time >= self.route_details[-1]['departure_time']:
            return self.route_details[-1]
        for d in self.route_details:
            if time > d['departure_time']:
                continue
            else:
                if isinstance(d['node'], Store):
                    uncollected_orders = [i for i in d['status_change'] if self.orders[i].ready_time>time]
                    d_copy = deepcopy(d)
                    for i in uncollected_orders:
                        d_copy['orders_collected'][i] = False
                    return d_copy
                else:
                    return d