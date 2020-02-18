"""
Functionality to allow inventory management for HP Norton.
"""

import csv

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Add a new record to the CSV invoice_file in this format:

    customer_name,item_code,item_description,item_monthly_price
    """
    with open(invoice_file, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow([customer_name, item_code, item_description, item_monthly_price])


#def single_customer(customer_name, invoice_file):
