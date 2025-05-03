class Discount:
    def __init__(self, name, percentage, ticket_type):
        self.__name = name  # e.g., "Weekend Promo"
        self.__percentage = percentage  # e.g., 10 for 10%
        self.__ticket_type = ticket_type  # e.g., "WeekendPackage"
        self.__active = True

    # Getters
    def get_name(self):
        return self.__name

    def get_percentage(self):
        return self.__percentage

    def get_ticket_type(self):
        return self.__ticket_type

    def is_active(self):
        return self.__active

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_percentage(self, percentage):
        self.__percentage = percentage

    def set_ticket_type(self, ticket_type):
        self.__ticket_type = ticket_type

    def activate(self):
        self.__active = True

    def deactivate(self):
        self.__active = False

    # Apply discount to a base price
    def apply_discount(self, base_price):
        if self.__active:
            return round(base_price * (1 - self.__percentage / 100), 2)
        return base_price

    def __str__(self):
        status = "Active" if self.__active else "Inactive"
        return f"{self.__name} ({self.__percentage}% off for {self.__ticket_type}) – {status}"
