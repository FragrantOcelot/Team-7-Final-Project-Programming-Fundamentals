# Import tkinter for GUI components and messagebox for pop-up alerts
import tkinter as tk
from tkinter import messagebox

# Import core logic and shared GUI utilities
from ticket_manager import TicketManager
from customer import Customer
from admin import Admin
from data_manager import DataManager
from ticket_types import SingleRaceTicket, WeekendPackage, SeasonPass, GroupDiscountTicket
from discount import Discount
from shared_gui_utils import clear_screen
from customer_views import show_customer_menu
from admin_views import show_admin_menu

# Initialize TicketManager and DataManager
tm = TicketManager()
dm = DataManager()

# Register available ticket types at app start
tm.register_ticket_type(SingleRaceTicket())
tm.register_ticket_type(WeekendPackage())
tm.register_ticket_type(SeasonPass())
tm.register_ticket_type(GroupDiscountTicket(5))
tm.register_ticket_type(GroupDiscountTicket(10))  # Optional larger group

tm._TicketManager__sales_log = dm.load_sales()

# Add discounts
disc1 = Discount("Weekend Promo", 10, "Weekend Package")
disc2 = Discount("Season Special", 15, "Season Pass")
disc3 = Discount("Expired Offer", 50, "Single Race Pass")
disc3.deactivate()  # Simulate expired discount

tm.add_discount(disc1)
tm.add_discount(disc2)
tm.add_discount(disc3)


# Load all users from storage
users = dm.load_users()

# Create and add a new admin
new_admin = Admin("Dr. Andrew", "admin@example.com", "admin123")
users.append(new_admin)
dm.save_users(users)

# Separate loaded users by role
customers = [u for u in users if isinstance(u, Customer)]
admins = [u for u in users if isinstance(u, Admin)]

# Initialize the main application window
root = tk.Tk()
root.title("Grand Prix Ticketing System")
root.geometry("400x300")  # Set fixed window size

# -------------------------
# Registration Screen
# -------------------------
def show_registration():
    clear_screen(root)  # Clear any previous widgets
    tk.Label(root, text="Register", font=("Arial", 16)).pack(pady=10)

    # Name input
    tk.Label(root, text="Name").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Email input
    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    # Password input
    tk.Label(root, text="Password").pack()
    pass_entry = tk.Entry(root, show="*")
    pass_entry.pack()

    # Triggered when "Register" button is clicked
    def register_action():
        name = name_entry.get()
        email = email_entry.get()
        password = pass_entry.get()

        # Validate input fields
        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            # Check if email already exists
            for user in customers + admins:
                if user.get_email() == email:
                    raise ValueError("Email already exists.")

            # Create new customer and save
            new_customer = Customer(name, email, password)
            customers.append(new_customer)
            users.append(new_customer)
            dm.save_users(users)

            messagebox.showinfo("Success", "Account created. Please login.")
            show_login()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    # Buttons for registration and back
    tk.Button(root, text="Register", command=register_action).pack(pady=10)
    tk.Button(root, text="Back to Login", command=lambda: show_login()).pack(pady=5)

# -------------------------
# Login Screen
# -------------------------
def show_login():
    clear_screen(root)
    tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=10)

    # Email input
    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    # Password input
    tk.Label(root, text="Password").pack()
    pass_entry = tk.Entry(root, show="*")
    pass_entry.pack()

    # Triggered when "Login" button is clicked
    def login_action():
        email = email_entry.get()
        password = pass_entry.get()
        try:
            # Check if credentials match any user
            for user in customers + admins:
                if user.get_email() == email and user.check_password(password):
                    messagebox.showinfo("Success", f"Welcome, {user.get_name()}")
                    if isinstance(user, Customer):
                        show_customer_menu(user, root, tm, dm)
                    else:
                        show_admin_menu(user, root, tm, dm)
                    return
            raise ValueError("Invalid email or password.")
        except ValueError as ve:
            messagebox.showerror("Login Failed", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error during login: {str(e)}")

    # Buttons for login and switch to register screen
    tk.Button(root, text="Login", command=login_action).pack(pady=10)
    tk.Button(root, text="Register", command=lambda: show_registration()).pack(pady=5)

# -------------------------
# Launch Application
# -------------------------
show_login()  # Start at the login screen
root.mainloop()  # Enter tkinter main loop
