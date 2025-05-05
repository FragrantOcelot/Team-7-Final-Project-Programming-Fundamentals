import uuid
from datetime import datetime

class PurchaseOrder:
    def __init__(self, customer_id, tickets, total_price, payment_method):
        self.__order_id = str(uuid.uuid4())
        self.__customer_id = customer_id
        self.__tickets = tickets  # list of Ticket objects
        self.__total_price = total_price
        self.__payment_method = payment_method  # e.g., "Credit Card", "Apple Pay"
        self.__purchase_time = datetime.now()

    # Getters only – no setters because this is a finalized record
    def get_order_id(self):
        return self.__order_id

    def get_customer_id(self):
        return self.__customer_id

    def get_tickets(self):
        return self.__tickets

    def get_total_price(self):
        return self.__total_price

    def get_payment_method(self):
        return self.__payment_method

    def get_purchase_time(self):
        return self.__purchase_time

    # String version for summaries
    def __str__(self):
        ticket_names = ', '.join([ticket.get_name() for ticket in self.__tickets])
        return (f"Order ID: {self.__order_id[:8]} | "
                f"Tickets: {ticket_names} | "
                f"Total: AED {self.__total_price} | "
                f"Payment: {self.__payment_method} | "
                f"Time: {self.__purchase_time.strftime('%Y-%m-%d %H:%M')}")
