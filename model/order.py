import datetime
from dataclasses import dataclass


@dataclass
class Order:
    order_id: int
    customer_id: int
    order_status: int
    order_date: datetime.datetime
    required_date: datetime.datetime
    shipped_date: datetime.datetime
    store_id : int
    staff_id:int

    def __hash__(self):
        return hash(self.order_id)
    def __eq__(self, other):
        return self.order_id == other.order_id
    def __str__(self):
        return f'Order({self.order_id}) effettuato in data { self.order_date}'