"""
Module for testing unit function.
"""
import sys
sys.path.append("../src")
from unittest import TestCase
from basic_operations import *
from customer_model import *


class BasicOperationsTest(TestCase):
    """Testing basic_operations module."""

    def setUp(self):
        """Multi-use dicts and lists for testing."""
        DATABASE.drop_tables([Customer])
        DATABASE.create_tables([Customer])
        DATABASE.close()

        self.customer_list = ['1234',
                              'Fun',
                              'Guy',
                              'Mushroom Lane',
                              '555-5555',
                              'fungi276@hotmail.com',
                              'active',
                              100000
                              ]

        self.customer_dict = {'customer_id': '1234',
                              'name': 'Fun',
                              'lastname': 'Guy',
                              'home_address': 'Mushroom Lane',
                              'phone_number': '555-5555',
                              'email_address': 'fungi276@hotmail.com',
                              'status': 'active',
                              'credit_limit': 100000
                              }

    def test_add_customer(self):
        """Confirm new customer data is added to db via add_customer."""
        add_customer(*self.customer_list)
        customer = Customer.get(Customer.customer_id == self.customer_list[0])
        self.assertEqual(customer.name, self.customer_dict['name'])

    def test_search_customer(self):
        """Confirm search_customer returns dict with customer data from a customer id"""
        add_customer(*self.customer_list)
        self.assertEqual(search_customer(self.customer_list[0]), self.customer_dict)

    def test_search_customer_none(self):
        """Test search function returns empty dict if no customer found."""
        self.assertEqual(search_customer('5678'), {})

    def test_delete_customer(self):
        """Test customer deletion."""
        add_customer(*self.customer_list)
        delete_customer(self.customer_list[0])
        self.assertEqual(search_customer(self.customer_list[0]), {})

    def test_delete_customer_none(self):
        """Test exception handling on delete_customer."""
        add_customer(*self.customer_list)
        with self.assertRaises(DoesNotExist):
            delete_customer('5678')

    def test_update_customer_credit(self):
        """Confirm customer at customer_id gets updated credit limit."""
        add_customer(*self.customer_list)
        update_customer_credit(self.customer_list[0], 0)
        customer = Customer.get(Customer.customer_id == self.customer_list[0])
        self.assertEqual(customer.credit_limit,0)

    def test_update_customer_credit_exception(self):
        """Confirm 'update_customer_credit' raises ValueError on non-existent customer."""
        with self.assertRaises(ValueError):
            update_customer_credit('5678', 0)

    def test_list_active_customers(self):
        """Confirm correct number of customers is returned."""
        add_customer(*self.customer_list)
        self.assertEqual(list_active_customers(), 1)