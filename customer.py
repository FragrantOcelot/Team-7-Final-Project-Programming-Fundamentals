from user import User

class Customer(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.__purchase_history = []  # list of PurchaseOrder objects

    # Get purchase history
    def get_purchase_history(self):
        return self.__purchase_history

    # Add a purchase
    def add_purchase(self, purchase_order):
        self.__purchase_history.append(purchase_order)

    # Delete a purchase by ID
    def delete_purchase(self, purchase_id):
        self.__purchase_history = [
            p for p in self.__purchase_history if p.get_order_id() != purchase_id
        ]

    # Display all purchases
    def display_purchases(self):
        if not self.__purchase_history:
            print("No purchases found.")
        else:
            for purchase in self.__purchase_history:
                print(purchase)
