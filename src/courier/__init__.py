from config import Config

class Courier:

    def __init__(self, config=None):

        if config is None:
            config = Config()
        self.config = config

        self.orders = []
        self.route = None
