import pickle
import os

class DataManager:
    def __init__(self):
        self.__user_file = "users.pkl"
        self.__order_file = "orders.pkl"
        self.__discount_file = "discounts.pkl"
        self.__sales_file = "sales.pkl"

    # ---------- Generic Helpers ----------
    def __load_data(self, filename):
        if not os.path.exists(filename):
            return []
        with open(filename, "rb") as f:
            return pickle.load(f)

    def __save_data(self, filename, data):
        with open(filename, "wb") as f:
            pickle.dump(data, f)

    # ---------- User ----------
    def load_users(self):
        return self.__load_data(self.__user_file)

    def save_users(self, users):
        self.__save_data(self.__user_file, users)

    # ---------- Orders ----------
    def load_orders(self):
        return self.__load_data(self.__order_file)

    def save_orders(self, orders):
        self.__save_data(self.__order_file, orders)

    # ---------- Discounts ----------
    def load_discounts(self):
        return self.__load_data(self.__discount_file)

    def save_discounts(self, discounts):
        self.__save_data(self.__discount_file, discounts)

    # ---------- Sales Log ----------
    def load_sales(self):
        return self.__load_data(self.__sales_file)

    def save_sales(self, sales):
        self.__save_data(self.__sales_file, sales)
