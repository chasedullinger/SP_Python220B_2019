"""
Class for the interactions of the database
"""
#pylint: disable=invalid-name
#pylint: disable=too-many-locals
import csv
import logging
from pymongo import MongoClient

#format for the log
LOG_FORMAT = "%(asctime)s %(filename)s: %(lineno)-3d %(levelname)s %(message)s"

#setup for formatter and log file
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = 'db.log'

#setup for file hanlder at error level
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode='w')
FILE_HANDLER.setLevel(30)
FILE_HANDLER.setFormatter(FORMATTER)

#setup for console handler at debug level
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(10)
CONSOLE_HANDLER.setFormatter(FORMATTER)

#setup for logging set at debug level
LOGGER = logging.getLogger()
LOGGER.setLevel(10)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

#dict to convert debug input to log level
LOG_LEVEL = {'0': 51, '1': 40, '2': 30, '3': 10}

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        logging.debug('Connecting to Mongo Database')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.debug('Closing Mongo Database')
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Takes a directory name three csv files on input (product data, customer data, rentals
    data) and populates new mongo DB and returns two tuples (record count of number or products
    customers, rentals added) (second with count of number of errors occured)
    """
    logging.debug('Attempting to import file data')
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton

        file_list = (product_file, customer_file, rentals_file)
        logging.debug('Successfully obtained file list')
        record_count = []
        error_count = []
        products = db['products']
        customers = db['customers']
        rentals = db['rentals']
        database_list = (products, customers, rentals)
        logging.debug('Got database list, going through files now')
        for filename, database in zip(file_list, database_list):
            errors = 0
            logging.debug('Attempting to open %s/%s', directory_name, filename)
            try:
                with open(directory_name + "/" + filename) as file:

                    csv_dict = csv.DictReader(file, delimiter=',')
                    logging.debug('Opened csv file %s', file)
                    list_data = []
                    logging.debug('Lopping through data in csv file')
                    for row in csv_dict:
                        list_data.append(row)

                    logging.debug('Attempting to insert data in database')
                    database.insert_many(list_data)
                    record_count.append(len(list_data))
                    logging.debug('Successfully added data into database')
            except FileNotFoundError:
                logging.error('Could not open file %s', filename)
                errors += 1
                record_count.append(None)

            error_count.append(errors)

    return tuple(record_count), tuple(error_count)


def show_available_products():
    """
    Returns a dict of products available
    """
    logging.debug('Attempting to show all available products')
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton

        products = db['products']
        products_dict = {}
        logging.debug('Attempting to loop through products')
        for item in products.find():
            query = {'description': item['description'],
                     'product_type': item['product_type'],
                     'quantity_available': item['quantity_available']}
            quantity_available = int(item['quantity_available'])
            if quantity_available > 0:
                products_dict[item['product_id']] = query
                logging.debug('Added product %s', query)

    logging.debug('Successfully showed all products')
    return products_dict



def show_rentals(product_id):
    """
    Returns dict with user ID, name, address, phone number, email information
    from users renting products
    """
    logging.debug('Attempting to show rentals')
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton

        customers = db['customers']
        rentals = db['rentals']
        customers_list = []
        rentals_dict = {}
        logging.debug('Attempting to loop through rentals to get user IDs')
        for item in rentals.find():
            if item['product_id'] == product_id:
                customers_list.append(item['user_id'])
                logging.debug('Obtained user %s', item['user_id'])

        logging.debug('Attempting to loop through customers and match rentals')
        for item in customers.find():

            query = {'name': item['name'],
                     'address': item['address'],
                     'phone_number': item['phone_number'],
                     'email': item['email']}
            if item['user_id'] in customers_list:
                rentals_dict[item['user_id']] = query
                logging.debug('Obtained rental for user %s', item['user_id'])

        logging.debug('Successfully showed all rentals')
        return rentals_dict
