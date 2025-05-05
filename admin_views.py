# Import tkinter GUI components
import tkinter as tk
from tkinter import messagebox

# Import shared function to reset screen
from shared_gui_utils import clear_screen

# ----------------------------------------
# ADMIN DASHBOARD MENU
# ----------------------------------------
def show_admin_menu(admin, root, tm, dm):
    clear_screen(root)
    tk.Label(root, text=f"Admin Panel – {admin.get_name()}", font=("Arial", 14)).pack(pady=10)

    # Admin options: view sales or manage discounts
    tk.Button(root, text="View Sales", command=lambda: view_sales(root, tm)).pack(pady=5)
    tk.Button(root, text="Manage Discounts", command=lambda: manage_discounts(admin, root, tm, dm)).pack(pady=5)
    tk.Button(root, text="Logout", command=lambda: root.quit()).pack(pady=20)

# ----------------------------------------
# VIEW SALES REPORT
# ----------------------------------------
def view_sales(root, tm):
    try:
        sales = tm.get_sales_report()
        if not sales:
            raise ValueError("No sales data available.")

        # Format each sales entry into a readable string
        formatted = "\n".join([f"{k}: {v} tickets" for k, v in sales.items()])
        messagebox.showinfo("Sales Report", formatted)

    except ValueError as ve:
        messagebox.showwarning("No Data", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load sales report: {str(e)}")

# ----------------------------------------
# DISCOUNT MANAGEMENT INTERFACE
# ----------------------------------------
def manage_discounts(admin, root, tm, dm):
    try:
        clear_screen(root)
        tk.Label(root, text="Manage Discounts", font=("Arial", 14)).pack(pady=10)

        # Combine active and inactive discounts for display
        discounts = tm.get_active_discounts() + [d for d in tm._TicketManager__discounts if not d.is_active()]

        # Display each discount with a toggle button
        for discount in discounts:
            frame = tk.Frame(root)
            frame.pack(pady=5, padx=10, fill="x")

            status = "Active" if discount.is_active() else "Inactive"
            text = f"{discount.get_name()} ({discount.get_percentage()}% off for {discount.get_ticket_type()}) – {status}"
            tk.Label(frame, text=text).pack(side="left")

            # Button to activate/deactivate the discount
            def toggle(d=discount):
                try:
                    if d.is_active():
                        d.deactivate()
                    else:
                        d.activate()
                    messagebox.showinfo("Updated", f"{d.get_name()} is now {'Active' if d.is_active() else 'Inactive'}")

                    # Refresh screen
                    manage_discounts(root, tm)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to toggle discount: {str(e)}")

            tk.Button(frame, text="Toggle", command=toggle).pack(side="right")

        # Back to admin menu
        tk.Button(root, text="Back", command=lambda: show_admin_menu(admin, root, tm, dm)).pack(pady=20)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load discounts: {str(e)}")
