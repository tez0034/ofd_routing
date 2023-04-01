from env import Environment
from courier import Courier
from dispatch.order import Order
from config import Config
from sim.state import State

import numpy as np
from typing import List, Union

class Simulator:

    def __init__(self, env:Union[dict, Environment]=None, 
                 couriers:List[Union[tuple, Courier]]=None, 
                 orders:List[Order]=None, 
                 config:Config=None, time:float=0.):
        if config is None:
            self.config = Config()
        env = self.init_env(env)
        couriers = self.init_couriers(couriers)
        orders = self.init_orders(orders)
        time = 0.

        self.state = State(env=env, couriers=couriers,
                           orders=orders, config=self.config,
                           time=time)
        

    def get_state(self) -> State:
        return self.state

    def step(self, t):
        pass
    
    @staticmethod
    def init_env(env)->Environment:
        try:
            if env is None:
                return Environment(format='random')
            elif isinstance(env, Environment):
                return env
            elif isinstance(env, dict):
                return Environment(env_graph=env)
            else:
                raise Exception(f'input env must be None or of type Environment or dict,\
                                 but is instead {type(env)}')
        except Exception as ee:
            raise Exception(f'Failed to initialize Environment: {ee}')
    
    def init_couriers(self, couriers)-> List[Courier]:
        if isinstance(couriers, list):
            if all([isinstance(courier, Courier) for courier in couriers]):
                return couriers
            elif all([isinstance(loc, tuple) for loc in couriers]):
                return list(map(lambda loc: Courier(location=loc,
                                                    subgraph=self.env.extract_subgraph_in_proximity(location=loc)), 
                                couriers))
            else:
                raise Exception(f'Argument couriers cannot be processed; couriers={couriers} ')
        elif couriers is None:
            n_couriers = self.config.random_init_n_couriers
            locations = np.random.uniform(size=[n_couriers, 2])
            locations = locations * np.array(self.config.map_size)
            return list(map(lambda loc: Courier(location=loc,
                                                subgraph=self.env.extract_subgraph_in_proximity(location=loc)), 
                            locations))
        else:
            raise Exception(f'Argument couriers should be either of type \
                             list of None but has type {type(couriers)}')
        
    def init_orders(self, orders) -> List[Order]:
        if isinstance(orders, list):
            if all([isinstance(order, Order) for order in orders]):
                return orders
            else:
                raise Exception(f'Argument orders cannot be processed; orders={orders} ')
        elif orders is None:
            return []
        else:
            raise Exception(f'Argument orders should be either of type \
                             list of None but has type {type(orders)}')

