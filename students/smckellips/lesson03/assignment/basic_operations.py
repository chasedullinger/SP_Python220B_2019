# pylint: disable=R0913,W0401,W0614
'''basic operations module.  For access from front_end.'''
import logging
from peewee import *
from customer_model import Customer, DB

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    '''add new customer function.'''
    try:
        with DB.atomic():
            Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit
            )
    except IntegrityError:
        LOGGER.warning("Customer ID %s is already taken.", customer_id)

def search_customer(customer_id):
    '''locate customer by id and return as dictionary.'''
    try:
        result = Customer.select().where(Customer.customer_id == customer_id).dicts().get()
    # except CustomerDoesNotExist as e:
    #     print(e)
    except DoesNotExist:
        result = {}
    return result

def delete_customer(customer_id):
    '''delete a customer by id.'''
    try:
        with DB.atomic():
            delete_query = Customer.delete().where(Customer.customer_id == customer_id)
            delete_query.execute()
    except IntegrityError:
        LOGGER.warning("Customer ID %s not found.", customer_id)

def update_customer_credit(customer_id, credit_limit):
    '''update a customers credit limit by id.'''
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
    except DoesNotExist:
        raise ValueError

def list_active_customers():
    '''list number of active customers.'''
    return Customer.select().where(Customer.status).count()
