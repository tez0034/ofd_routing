from config import Config
from env.store import Store
from env.customer import Customer

class Order:

    def __init__(self, customer:Customer, store:Store, deadline, creation_time, config=None):

        if config is None:
            config = Config()
        self.config = config

        self.customer = customer
        self.store = store
        self.deadline = deadline
        self.creation_time = creation_time
        self.ready_time = creation_time + self.store.wait_time
        self.collected = False
        self.completed = False
        self.courier = None

    def calculate_cost(self, completion_time):
        # TODO: change this tentative formula
        if completion_time > self.deadline:
            return self.deadline - self.creation_time \
                    + (completion_time - self.deadline)*self.config.late_penalty_weight\
                    + self.config.late_penalty_constant
