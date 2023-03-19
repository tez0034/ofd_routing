from config import Config

class Order:

    def __init__(self, customer, store, deadline, creation_time, config=None):

        if config is None:
            config = Config()
        self.config = config

        self.customer = customer
        self.store = store
        self.deadline = deadline
        self.creation_time = creation_time
        self.collected = False
        self.completed = False
        self.courier = None

    def calculate_cost(self, completion_time):
        # TODO: change this tentative formula
        if completion_time > self.deadline:
            return self.deadline - self.creation_time \
                    + (completion_time - self.deadline)*self.config.late_penalty_weight\
                    + self.config.late_penalty_constant
