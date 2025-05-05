# customer_views.py
# Handles all customer-facing GUI: main menu, profile editing, ticket purchase, and purchase history (view/edit/delete)

import tkinter as tk
from tkinter import messagebox
from purchase_order import PurchaseOrder
from shared_gui_utils import clear_screen

# ----------------------------------------
# CUSTOMER MAIN MENU
# ----------------------------------------
def show_customer_menu(customer, root, tm, dm):
    clear_screen(root)
    tk.Label(root, text=f"Welcome, {customer.get_name()}", font=("Arial", 14)).pack(pady=10)

    # New: Edit Profile button
    tk.Button(
        root,
        text="Edit Profile",
        command=lambda: show_edit_profile(customer, root, tm, dm)
    ).pack(pady=5)

    tk.Button(
        root,
        text="View Purchases",
        command=lambda: view_purchases(customer, root, tm, dm)
    ).pack(pady=5)
    tk.Button(
        root,
        text="Buy Tickets",
        command=lambda: buy_ticket(customer, root, tm, dm)
    ).pack(pady=5)
    tk.Button(root, text="Logout", command=lambda: root.quit()).pack(pady=20)


# ----------------------------------------
# PROFILE EDITING
# ----------------------------------------
def show_edit_profile(customer, root, tm, dm):
    clear_screen(root)
    tk.Label(root, text="Edit Profile", font=("Arial", 14)).pack(pady=10)

    # Pre-filled entries
    tk.Label(root, text="Name").pack()
    name_entry = tk.Entry(root)
    name_entry.insert(0, customer.get_name())
    name_entry.pack()

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root)
    email_entry.insert(0, customer.get_email())
    email_entry.pack()

    tk.Label(root, text="Password (leave blank to keep)").pack()
    pass_entry = tk.Entry(root, show="*")
    pass_entry.pack()

    def save_profile():
        new_name = name_entry.get().strip()
        new_email = email_entry.get().strip()
        new_pass = pass_entry.get()

        if not new_name or not new_email:
            messagebox.showerror("Error", "Name and email cannot be empty.")
            return

        try:
            customer.set_name(new_name)
            customer.set_email(new_email)
            if new_pass:
                customer.set_password(new_pass)
            dm.save_users([customer])
            messagebox.showinfo("Success", "Profile updated.")
            show_customer_menu(customer, root, tm, dm)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {e}")

    tk.Button(root, text="Save", command=save_profile).pack(pady=10)
    tk.Button(root, text="Cancel", command=lambda: show_customer_menu(customer, root, tm, dm)).pack(pady=5)


# ----------------------------------------
# TICKET PURCHASING INTERFACE
# ----------------------------------------
def buy_ticket(customer, root, tm, dm):
    clear_screen(root)
    tk.Label(root, text="Buy Ticket", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Select Ticket Type").pack()
    tickets = tm.get_available_ticket_types()
    ticket_var = tk.StringVar(value=tickets[0] if tickets else "")
    tk.OptionMenu(root, ticket_var, *tickets).pack()

    tk.Label(root, text="Payment Method").pack()
    payment_var = tk.StringVar(value="Credit Card")
    tk.OptionMenu(root, payment_var, "Credit Card", "Debit Card", "Apple Pay", "Google Pay").pack()

    def confirm_purchase():
        try:
            name = ticket_var.get()
            ticket = tm.get_ticket_by_name(name)
            if ticket is None:
                raise ValueError("Invalid ticket selected.")
            price = tm.calculate_final_price(ticket)
            method = payment_var.get()

            order = PurchaseOrder(customer.get_user_id(), [ticket], price, method)
            customer.add_purchase(order)

            # Merge and save sales
            prev_sales = dm.load_sales()
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            prev_sales[today] = prev_sales.get(today, 0) + 1
            dm.save_sales(prev_sales)

            dm.save_users([customer])
            dm.save_orders(customer.get_purchase_history())

            messagebox.showinfo("Success", f"Purchased {ticket.get_name()} for AED {price}")
            show_customer_menu(customer, root, tm, dm)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Confirm Purchase", command=confirm_purchase).pack(pady=10)
    tk.Button(root, text="Back", command=lambda: show_customer_menu(customer, root, tm, dm)).pack(pady=5)


# ----------------------------------------
# VIEW, EDIT & DELETE PURCHASES
# ----------------------------------------
def view_purchases(customer, root, tm, dm):
    clear_screen(root)
    tk.Label(root, text="Your Purchases", font=("Arial", 14)).pack(pady=10)

    purchases = customer.get_purchase_history()
    if not purchases:
        tk.Label(root, text="No purchases found.").pack(pady=10)
    else:
        for order in purchases:
            frame = tk.Frame(root)
            frame.pack(pady=3, padx=10, fill="x")

            tk.Label(
                frame,
                text=str(order),
                anchor="w",
                justify="left"
            ).pack(side="left", fill="x", expand=True)

            # Edit button
            tk.Button(
                frame,
                text="Edit",
                command=lambda o=order: show_edit_order(o, customer, root, tm, dm)
            ).pack(side="right", padx=(0,5))

            # Delete button
            tk.Button(
                frame,
                text="Delete",
                command=lambda o=order: delete_order(o, customer, root, tm, dm)
            ).pack(side="right")

    tk.Button(root, text="Back", command=lambda: show_customer_menu(customer, root, tm, dm)).pack(pady=20)


def delete_order(order, customer, root, tm, dm):
    try:
        customer.delete_purchase(order.get_order_id())
        dm.save_users([customer])
        dm.save_orders(customer.get_purchase_history())
        messagebox.showinfo("Deleted", "Order deleted.")
        view_purchases(customer, root, tm, dm)
    except Exception as e:
        messagebox.showerror("Error", f"Delete failed: {e}")


def show_edit_order(order, customer, root, tm, dm):
    clear_screen(root)
    tk.Label(root, text="Modify Order", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="Payment Method").pack()
    method_var = tk.StringVar(value=order.get_payment_method())
    tk.OptionMenu(root, method_var, "Credit Card", "Debit Card", "Apple Pay", "Google Pay").pack()

    def save_edit():
        try:
            new_method = method_var.get()
            tickets = order.get_tickets()
            total = order.get_total_price()
            new_order = PurchaseOrder(customer.get_user_id(), tickets, total, new_method)

            customer.delete_purchase(order.get_order_id())
            customer.add_purchase(new_order)

            dm.save_users([customer])
            dm.save_orders(customer.get_purchase_history())

            messagebox.showinfo("Success", "Order updated.")
            view_purchases(customer, root, tm, dm)
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    tk.Button(root, text="Save Changes", command=save_edit).pack(pady=10)
    tk.Button(root, text="Cancel", command=lambda: view_purchases(customer, root, tm, dm)).pack(pady=5)
