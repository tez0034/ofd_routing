from config import Config
from env.store import Store
from env.customer import Customer
import warnings

class Route:

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

        self.valid = self.is_valid()
        if not self.valid:
            warnings.warn('Route is invalid, calculate_cost method is disabled')
        
        self.process_route()

    def process_route(self):
        self.route_details = [{'node': self.node_sequence[0],
                               'time': self.courier_state['next_node_arrival_time']}]
        
        time = self.courier_state['next_node_arrival_time']
        prev_node = self.node_sequence[0]
        for node in self.node_sequence[1:]:
            time += prev_node.get_edge_attributes(node, 'travel_time') \
                    + (prev_node.wait_time if isinstance(prev_node, Store) else 0)
            self.route_details.append({'node':node, 'time':time})
            prev_node = node
        self.route_details_dict = {d['node'].name: d for d in self.route_details}
            
    def calculate_cost(self):
        cost = 0.
        for order in self.courier_state['orders']:
            if order.customer in self.node_sequence:
                # validity check ensures that the customer's orders has been collected
                cost += order.calculate_cost(self.route_details_dict[order.customer.name]['time'])
            else:
                # append tentative order cost based on time at end of route since order has 
                # not yet been delivered
                cost += order.calculate_cost(self.route_details[-1]['time'])
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
        time_list = [d['time'] for d in self.route_details]
        idx = list(map(lambda i: i > time, time_list)).index(True) \
                if max(time_list)>time else (len(time_list)-1)
        return self.route_details[idx]
        
