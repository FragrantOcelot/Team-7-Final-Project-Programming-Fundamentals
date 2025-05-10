import os
import shutil
import uuid
import pickle
import unittest
from datetime import datetime, timedelta

from ticket_manager import TicketManager
from customer import Customer
from purchase_order import PurchaseOrder
from admin import Admin
from discount import Discount
from ticket_types import (
    SingleRaceTicket, WeekendPackage, SeasonPass, GroupDiscountTicket
)
from data_manager import DataManager

class TestTicketManager(unittest.TestCase):
    def setUp(self):
        # fresh manager
        self.tm = TicketManager()
        # register ticket types
        self.t1 = SingleRaceTicket()
        self.t2 = WeekendPackage()
        self.t3 = SeasonPass()
        self.g5 = GroupDiscountTicket(5)
        self.tm.register_ticket_type(self.t1)
        self.tm.register_ticket_type(self.t2)
        self.tm.register_ticket_type(self.t3)
        self.tm.register_ticket_type(self.g5)

        # setup discounts
        self.d1 = Discount("Weekend Promo", 10, self.t2.get_name())
        self.d2 = Discount("Season Special", 15, self.t3.get_name())
        self.d3 = Discount("Expired", 50, self.t1.get_name())
        self.d3.deactivate()

        self.tm.add_discount(self.d1)
        self.tm.add_discount(self.d2)
        self.tm.add_discount(self.d3)

    def test_ticket_lookup(self):
        # registered tickets should be found
        self.assertIs(self.tm.get_ticket_by_name(self.t1.get_name()), self.t1)
        self.assertIs(self.tm.get_ticket_by_name(self.t2.get_name()), self.t2)
        self.assertIs(self.tm.get_ticket_by_name(self.t3.get_name()), self.t3)
        self.assertIs(self.tm.get_ticket_by_name(self.g5.get_name()), self.g5)
        # nonexistent ticket returns None
        self.assertIsNone(self.tm.get_ticket_by_name("No Such Ticket"))

    def test_calculate_final_price(self):
        # WeekendPackage has 10% off
        expected = round(self.t2.get_price() * 0.9, 2)
        self.assertEqual(self.tm.calculate_final_price(self.t2), expected)
        # SeasonPass has 15% off
        expected2 = round(self.t3.get_price() * 0.85, 2)
        self.assertEqual(self.tm.calculate_final_price(self.t3), expected2)
        # SingleRaceTicket discount is inactive, so full price
        self.assertEqual(self.tm.calculate_final_price(self.t1), self.t1.get_price())
        # Group ticket (no discount)
        self.assertEqual(self.tm.calculate_final_price(self.g5), self.g5.get_price())

    def test_sales_logging_and_report(self):
        today = datetime.now().strftime("%Y-%m-%d")
        # initially empty or no entry for today
        report = self.tm.get_sales_report()
        self.assertNotIn(today, report)

        # record some sales
        self.tm.record_sale(3)
        rep = self.tm.get_sales_report()
        self.assertEqual(rep[today], 3)

        self.tm.record_sale(2)
        rep2 = self.tm.get_sales_report()
        self.assertEqual(rep2[today], 5)


class TestCustomerAndPurchase(unittest.TestCase):
    def setUp(self):
        self.cust = Customer("Hamdan", "hamdan@example.com", "pass123")
        self.t1 = SingleRaceTicket()
        self.t2 = WeekendPackage()

    def test_purchase_history_crud(self):
        # no purchases initially
        self.assertEqual(self.cust.get_purchase_history(), [])

        # create orders
        price1 = 100.0
        order1 = PurchaseOrder(self.cust.get_user_id(), [self.t1, self.t2], price1, "Credit Card")
        self.cust.add_purchase(order1)
        hist = self.cust.get_purchase_history()
        self.assertEqual(len(hist), 1)
        self.assertIs(hist[0], order1)

        # delete purchase
        self.cust.delete_purchase(order1.get_order_id())
        self.assertEqual(self.cust.get_purchase_history(), [])

    def test_display_purchases_str(self):
        order = PurchaseOrder(self.cust.get_user_id(), [self.t1], self.t1.get_price(), "Apple Pay")
        self.cust.add_purchase(order)
        # display_purchases prints without error
        self.cust.display_purchases()

class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.admin = Admin("Dr Andrew", "admin@example.com", "adminpass")

    def test_admin_id_and_str(self):
        aid = self.admin.get_admin_id()
        self.assertTrue(aid.startswith("ADM-"))
        s = str(self.admin)
        self.assertIn("Admin:", s)
        self.assertIn(self.admin.get_name(), s)
        self.assertIn(self.admin.get_email(), s)

class TestTicketTypes(unittest.TestCase):
    def test_single_and_weekend(self):
        s = SingleRaceTicket()
        self.assertEqual(s.get_name(), "Single Race Pass")
        self.assertEqual(s.get_price(), 300.0)
        self.assertEqual(s.get_validity(), "One Day")
        self.assertIn("Access to one race", s.get_features())

        w = WeekendPackage()
        self.assertEqual(w.get_name(), "Weekend Package")
        self.assertEqual(w.get_price(), 750.0)
        self.assertEqual(w.get_validity(), "Three Days")

    def test_season_and_group(self):
        sp = SeasonPass()
        self.assertEqual(sp.get_name(), "Season Pass")
        self.assertGreater(sp.get_price(), 0)

        g4 = GroupDiscountTicket(4)
        unit = max(250.0, 300.0 - 4*5)
        self.assertEqual(g4.get_price(), unit * 4)
        self.assertEqual(g4.get_group_size(), 4)

class TestPurchaseOrder(unittest.TestCase):
    def setUp(self):
        self.t = SingleRaceTicket()
        self.order = PurchaseOrder("cust123", [self.t], self.t.get_price(), "Debit Card")

    def test_getters_and_str(self):
        oid = uuid.UUID(self.order.get_order_id())  # valid uuid
        self.assertEqual(self.order.get_customer_id(), "cust123")
        self.assertEqual(self.order.get_tickets(), [self.t])
        self.assertEqual(self.order.get_total_price(), self.t.get_price())
        self.assertEqual(self.order.get_payment_method(), "Debit Card")
        # purchase time recent
        now = datetime.now()
        self.assertTrue(now - self.order.get_purchase_time() < timedelta(seconds=1))

        s = str(self.order)
        self.assertIn("Order ID:", s)
        self.assertIn(self.t.get_name(), s)
        self.assertIn("Total:", s)
        self.assertIn("Payment:", s)

class TestDataManager(unittest.TestCase):
    TEST_DIR = "dm_test"

    def setUp(self):
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
        os.mkdir(self.TEST_DIR)
        self.dm = DataManager()
        # override default files into TEST_DIR
        self.dm._DataManager__user_file = os.path.join(self.TEST_DIR, "users.pkl")
        self.dm._DataManager__order_file = os.path.join(self.TEST_DIR, "orders.pkl")
        self.dm._DataManager__discount_file = os.path.join(self.TEST_DIR, "discounts.pkl")
        self.dm._DataManager__sales_file = os.path.join(self.TEST_DIR, "sales.pkl")

    def tearDown(self):
        shutil.rmtree(self.TEST_DIR)

    def test_users_persistence(self):
        users = [Customer("A","a@x.com","pw"), Customer("B","b@x.com","pw2")]
        self.dm.save_users(users)
        loaded = self.dm.load_users()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].get_email(), "a@x.com")

    def test_orders_persistence(self):
        o = PurchaseOrder("c", [SingleRaceTicket()], 300.0, "card")
        self.dm.save_orders([o])
        loaded = self.dm.load_orders()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].get_customer_id(), "c")

    def test_discounts_persistence(self):
        d = Discount("Test", 20, SingleRaceTicket().get_name())
        self.dm.save_discounts([d])
        loaded = self.dm.load_discounts()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].get_name(), "Test")

    def test_sales_persistence(self):
        sales = {"2025-05-10": 8}
        self.dm.save_sales(sales)
        loaded = self.dm.load_sales()
        self.assertIsInstance(loaded, dict)
        self.assertEqual(loaded.get("2025-05-10"), 8)

if __name__ == "__main__":
    unittest.main()
