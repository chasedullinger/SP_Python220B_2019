"""Furniture class"""
from inventory_management.inventory_class import Inventory
# import line changed to allow import of module in a nested folder


class Furniture(Inventory):
    """Using the Inventory base object, creates an inventory object for furniture and adds
    additional furniture specific attributes"""

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        Inventory.__init__(self, product_code, description, market_price, rental_price)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
