from dispatch.order import Order
from courier import Courier
from config import Config
from env import Environment

from typing import List
import numpy as np

class Dispatch:

    def __init(self, config=None):
        if config is None:
            config = Config()
        

    def assign_order(self, order:Order, courier:Courier):
        order.courier = courier
        courier.orders.append(order)
    
    def baseline(self, new_orders:List[Order], couriers:List[Courier]):
        locations = np.array([c.get_state['next_node'].location if c.route is not None 
                              else c.initial_location for c in couriers])
        for order in new_orders:
            nearest_courier = np.argmin(np.sum((locations - 
                                                np.array(order.store.location)[np.newaxis,:])**2, 
                                               axis=1))
            self.assign_order(order, couriers[nearest_courier])
    
    def dispatch(self, new_orders:List[Order], couriers:List[Courier], env:Environment):
        return self.baseline(new_orders=new_orders, couriers=couriers)
