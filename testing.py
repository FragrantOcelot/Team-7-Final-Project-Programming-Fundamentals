from ticket_manager import TicketManager
from customer import Customer
from purchase_order import PurchaseOrder
from admin import Admin
from discount import Discount
from ticket_types import (
    SingleRaceTicket, WeekendPackage, SeasonPass, GroupDiscountTicket,
)
from data_manager import DataManager

# Initialize TicketManager and register ticket types
tm = TicketManager()
tm.register_ticket_type(SingleRaceTicket())
tm.register_ticket_type(WeekendPackage())
tm.register_ticket_type(SeasonPass())
tm.register_ticket_type(GroupDiscountTicket(5))
tm.register_ticket_type(GroupDiscountTicket(10))  # Edge case

# Add discounts
disc1 = Discount("Weekend Promo", 10, "Weekend Package")
disc2 = Discount("Season Special", 15, "Season Pass")
disc3 = Discount("Expired Offer", 50, "Single Race Pass")
disc3.deactivate()  # Simulate expired discount

tm.add_discount(disc1)
tm.add_discount(disc2)
tm.add_discount(disc3)

# Create users
cust1 = Customer("Hamdan", "hamdan@example.com", "pass123")
cust2 = Customer("Zayed", "zayed@uni.ac.ae", "secure456")
admin = Admin("Dr. Andrew", "admin@example.com", "adminpass")

# Customer 1 makes a purchase with two discounted tickets
t1 = tm.get_ticket_by_name("Weekend Package")
t2 = tm.get_ticket_by_name("Season Pass")
p1_price = tm.calculate_final_price(t1)
p2_price = tm.calculate_final_price(t2)
order1 = PurchaseOrder(cust1.get_user_id(), [t1, t2], p1_price + p2_price, "Credit Card")
cust1.add_purchase(order1)
tm.record_sale(2)

# Customer 2 makes a purchase of a group ticket without discount
t3 = tm.get_ticket_by_name("Group Ticket (5 people)")
order2 = PurchaseOrder(cust2.get_user_id(), [t3], t3.get_price(), "Apple Pay")
cust2.add_purchase(order2)
tm.record_sale(5)

# Customer 1 makes another purchase with no discount
t4 = tm.get_ticket_by_name("Single Race Pass")
order3 = PurchaseOrder(cust1.get_user_id(), [t4], t4.get_price(), "Debit Card")
cust1.add_purchase(order3)
tm.record_sale(1)

# Display summaries
print("=== PURCHASE ORDERS ===")
for order in cust1.get_purchase_history():
    print(order)

for order in cust2.get_purchase_history():
    print(order)

print("\n=== SALES REPORT ===")
print(tm.get_sales_report())

print("\n=== ACTIVE DISCOUNTS ===")
for d in tm.get_active_discounts():
    print(d)

# Save all to files
dm = DataManager()
dm.save_users([cust1, cust2, admin])
dm.save_orders(cust1.get_purchase_history() + cust2.get_purchase_history())
dm.save_discounts(tm.get_active_discounts())
dm.save_sales(tm.get_sales_report())

# Reload and check
print("\n=== RELOADED USERS ===")
users = dm.load_users()
for u in users:
    print(u)

print("\n=== RELOADED ORDERS ===")
orders = dm.load_orders()
for o in orders:
    print(o)

print("\n=== RELOADED SALES LOG ===")
print(dm.load_sales())
