from env import Environment
from courier import Courier
from dispatch.order import Order
from config import Config

import numpy as np
from typing import List, Union

class State:

    def __init__(self, env:Environment=None, 
                 couriers:List[Courier]=None, 
                 orders:List[Order]=None, 
                 config:Config=None, time:float=0.):
        
        if config is not None:
            config = Config()
        
        self.orders = orders
        self.couriers = couriers
        self.env = env
        self.time = time

    def process_orders(self):
        self.orders_unassigned = []
        self.orders_assigned = []
        self.orders_collected = []
        self.orders_completed = []
        for o in self.orders:
            if o.completed:
                self.orders_completed.append(o)
            elif o.collected:
                self.orders_collected.append(o)
            elif o.courier is not None:
                self.orders_assigned.append(o)
            else:
                self.orders_unassigned.append(o)

    def step_to_time(self, t):
        # Update order status
        for courier in self.couriers:
            d = courier.route.get_current_state(t)
            for i in d['orders_completed']:
                courier.route.orders[i].completed = True
            for i in d['orders_collected']:
                courier.route.orders[i].collected = True

        # Get new orders and dispatch
        pass
