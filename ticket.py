import uuid

class Ticket:
    def __init__(self, name, price, validity, features):
        self.__ticket_id = str(uuid.uuid4())
        self.__name = name
        self.__price = price
        self.__validity = validity  # e.g., "One Day", "Weekend", "Season"
        self.__features = features  # list of features (strings)

    # Getters
    def get_ticket_id(self):
        return self.__ticket_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_validity(self):
        return self.__validity

    def get_features(self):
        return self.__features

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_validity(self, validity):
        self.__validity = validity

    def set_features(self, features):
        self.__features = features

    def __str__(self):
        return f"{self.__name} ({self.__validity}) - AED {self.__price}"
