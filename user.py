import uuid
from datetime import datetime

class User:
    def __init__(self, name, email, password):
        self.__user_id = str(uuid.uuid4())
        self.__name = name
        self.__email = email
        self.__password = password
        self.__created_at = datetime.now()

    # Getters
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_created_at(self):
        return self.__created_at

    # Setters
    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_password(self, new_password):
        self.__password = new_password

    # None for created_at because we never want to change it 

    # Password check
    def check_password(self, input_password):
        return self.__password == input_password

    # For printing
    def __str__(self):
        return f"{self.__name} ({self.__email})"
