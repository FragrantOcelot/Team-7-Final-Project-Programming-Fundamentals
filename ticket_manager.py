from datetime import datetime


class TicketManager:
    def __init__(self):
        self.__available_tickets = {}  # key: ticket_type name, value: Ticket subclass
        self.__discounts = []  # list of Discount objects
        self.__sales_log = {}  # key: date (yyyy-mm-dd), value: count of tickets sold

    # Register ticket type
    def register_ticket_type(self, ticket_obj):
        self.__available_tickets[ticket_obj.get_name()] = ticket_obj

    def get_available_ticket_types(self):
        return list(self.__available_tickets.keys())

    def get_ticket_by_name(self, name):
        return self.__available_tickets.get(name)

    # Discount handling
    def add_discount(self, discount):
        self.__discounts.append(discount)

    def get_active_discounts(self):
        return [d for d in self.__discounts if d.is_active()]

    def find_discount_for_ticket(self, ticket_type_name):
        for discount in self.__discounts:
            if discount.get_ticket_type() == ticket_type_name and discount.is_active():
                return discount
        return None

    # Calculate final price
    def calculate_final_price(self, ticket):
        discount = self.find_discount_for_ticket(ticket.get_name())
        if discount:
            return discount.apply_discount(ticket.get_price())
        return ticket.get_price()

    # Record sales
    def record_sale(self, quantity=1):
        today = datetime.now().strftime("%Y-%m-%d")
        self.__sales_log[today] = self.__sales_log.get(today, 0) + quantity

    def get_sales_report(self):
        return self.__sales_log
