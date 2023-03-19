from dispatch.order import Order
from courier import Courier

class Dispatch:

    def __init(self):
        pass

    def assign_order(self, order:Order, courier:Courier):
        order.courier = courier
        courier.orders.append(order)
