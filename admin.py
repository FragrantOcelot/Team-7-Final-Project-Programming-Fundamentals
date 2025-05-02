from user import User

class Admin(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.__admin_id = "ADM-" + self.get_user_id()[:8]  # Custom ID for UI clarity

    def get_admin_id(self):
        return self.__admin_id

    # In GUI: Admin will trigger these actions via TicketManager or DiscountManager
    def __str__(self):
        return f"Admin: {self.get_name()} ({self.get_email()})"
