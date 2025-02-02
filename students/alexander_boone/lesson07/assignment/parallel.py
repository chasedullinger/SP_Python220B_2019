'''Contains funcitons to manipulate Norton Furniture db.'''

import csv
import os
import time
import multiprocessing
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """Initialize MongoDB Database"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data_parallel(
        directory_name, product_file,
        customer_file, rentals_file):
    '''
    Takes a directory name and three csv files as input, one with product data,
    one with customer data and the third one with rentals data and creates
    and populates a new MongoDB database with these data. Returns 2 tuples:
    the first with a record count of the number of products, customers and
    rentals added (in that order), the second with a count of any errors that
    occurred, in the same order.
    '''
    start = time.time()

    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    # In order to avoid failure due to contention in the database,
    # I used separation of concerns to containerize access to each
    # collection in the database. Therefore, each process would call
    # one function with one dataset that would establish a
    # connection with a unique collection. This would avoid the
    # sharing of memory between processes, and since processes
    # don't/shouldn't share memory, this avoids contention.

    p1 = multiprocessing.Process(
        target=import_product_data,
        args=(directory_name, product_file, return_dict)
        )
    p2 = multiprocessing.Process(
        target=import_customer_data,
        args=(directory_name, customer_file, return_dict)
        )
    p3 = multiprocessing.Process(
        target=import_rental_data,
        args=(directory_name, rentals_file, return_dict)
        )

    jobs = [p1, p2, p3]

    for job in jobs:
        job.start()

    for job in jobs:
        job.join()

    runtime = time.time() - start

    # Before/after record counts
    product_tuple = (
        return_dict[0][0],
        return_dict[0][2],
        return_dict[0][3],
        runtime
        )
    cust_tuple = (
        return_dict[1][0],
        return_dict[1][2],
        return_dict[1][3],
        runtime
        )

    return [product_tuple, cust_tuple]


def import_product_data(directory_name, product_file, return_dict):
    '''Import product data to HP Norton DB.'''
    with client:
        db = client.connection.hp_norton

        # Create/open products collection
        products = db['products']
        prod_ct_before = products.count()

        # Assemble product file path
        product_path = os.path.join(directory_name, product_file)

        # Prepare function return counts
        counts_prod = 0
        error_counts_prod = 0

        # Load product data into db
        with open(product_path) as prod_file:
            product_reader = csv.reader(prod_file)

            # Iterate over first row to grab product data headers
            product_headers = next(product_reader)

            # Iterate over remaining rows to insert product data
            for row in product_reader:
                try:
                    products.insert_one(
                        {
                            product_headers[0]: row[0],
                            product_headers[1]: row[1],
                            product_headers[2]: row[2],
                            product_headers[3]: row[3]
                        }
                    )
                    counts_prod += 1
                except IndexError:
                    error_counts_prod += 1
        prod_ct_after = products.count()
    return_dict[0] = [
        counts_prod,
        error_counts_prod,
        prod_ct_before,
        prod_ct_after
        ]


def import_customer_data(directory_name, customer_file, return_dict):
    '''Import customer data to HP Norton DB.'''
    with client:
        db = client.connection.hp_norton

        # Create/open customer collection
        customers = db['customers']
        cust_ct_before = customers.count()

        # Assemble customer file path
        customer_path = os.path.join(directory_name, customer_file)

        # Prepare function return counts
        counts_cust = 0
        error_counts_cust = 0

        # Load customer data into db
        with open(customer_path) as cust_file:
            customer_reader = csv.reader(cust_file)

            # Iterate over first row to grab customer data headers
            customer_headers = next(customer_reader)

            # Iterate over remaining rows to insert customer data
            for row in customer_reader:
                try:
                    customers.insert_one(
                        {
                            customer_headers[0]: row[0],
                            customer_headers[1]: row[1],
                            customer_headers[2]: row[2],
                            customer_headers[3]: row[3],
                            customer_headers[4]: row[4]
                        }
                    )
                    counts_cust += 1
                except IndexError:
                    error_counts_cust += 1
        cust_ct_after = customers.count()
    return_dict[1] = [
        counts_cust,
        error_counts_cust,
        cust_ct_before,
        cust_ct_after
        ]


def import_rental_data(directory_name, rentals_file, return_dict):
    '''Import rental data to HP Norton DB.'''
    with client:
        db = client.connection.hp_norton

        # Create/open rentals collection
        rentals = db['rentals']

        # Assemble rentals file path
        rentals_path = os.path.join(directory_name, rentals_file)

        # Prepare function return counts
        counts_rentals = 0
        error_counts_rentals = 0

        # Load rental data into db
        with open(rentals_path) as rent_file:
            rentals_reader = csv.reader(rent_file)

            # Iterate over first row to grab customer data headers
            rentals_headers = next(rentals_reader)

            # Iterate over remaining rows to insert rentals data
            for row in rentals_reader:
                try:
                    rentals.insert_one(
                        {
                            rentals_headers[0]: row[0],
                            rentals_headers[1]: row[1]
                        }
                    )
                    counts_rentals += 1
                except IndexError:
                    error_counts_rentals += 1
        return_dict[2] = [counts_rentals, error_counts_rentals]


def show_available_products():
    '''
    Return a Python dictionary with the following user information
    from users that have rented products matching product_id:
    - user_id
    - name
    - address
    - phone number
    - email
    '''

    with client:
        db = client.connection.hp_norton

        # Create/open collections (AKA tables in RDBMS)
        products = db['products']

        available_products = dict()

        myquery = {"quantity_available": {"$gt": "0"}}
        product_iterator = products.find(myquery)
        for product in product_iterator:
            del product['_id']
            prod_id = product['product_id']
            del product['product_id']
            available_products[prod_id] = product
        return available_products


def show_rentals(product_id):
    '''
    Return a Python dictionary with the following user information
    from users that have rented products matching product_id:
    - user_id
    - name
    - address
    - phone number
    - email
    '''

    with client:
        db = client.connection.hp_norton

        # Create/open collections (AKA tables in RDBMS)
        customers = db['customers']
        rentals = db['rentals']

        users_dict = dict()

        myquery = {"product_id": product_id}
        rental_iterator = rentals.find(myquery)
        for rental in rental_iterator:
            user_query = {"user_id": rental["user_id"]}
            user = customers.find_one(user_query)
            del user['_id']
            del user['user_id']
            users_dict[rental["user_id"]] = user
    return users_dict


client = MongoDBConnection()
