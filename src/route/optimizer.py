from route import Route
from config import Config
from courier import Courier
from operator import attrgetter

class Optimizer:

    def __init__(self, config=None):
        if config is None:
            config = Config()
    
    def baseline(self, orders:list, courier:Courier, time):
        '''
        Initialize route for testing
        '''
        node_sequence = []
        orders = sorted(orders, key=attrgetter('deadline'))

        # get courier state 
        first_node = None if courier.route is not None else \
                    (orders[0].store if not orders[0].collected else orders[0].customer)
        courier_state = courier.get_state(time=time, next_node=first_node)

        # get node sequence
        node_sequence.append(courier_state['next_node'])
        if first_node is not None: # i.e. first node is from orders list
            if orders[0].store == courier_state['next_node']:
                node_sequence.append(orders[0].customer)
            orders = orders[1:]
        for order in orders:
            if order.completed:
                continue
            if not order.collected:
                node_sequence.append(order.store)
            node_sequence.append(order.customer)
        return Route(node_sequence=node_sequence, courier_state=courier_state)

