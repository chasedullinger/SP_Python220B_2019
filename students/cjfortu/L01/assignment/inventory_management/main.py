#!/usr/bin/env python
"""
This is the main interface and class handling module.

W0613 disabled in pylintrc.
Minimum methods set to 1 in pylintrc.
"""

import sys
import market_prices as mkt_prc
import inventory_class as inven_cl
import furniture_class as furn_cl
import electric_appliances_class as el_app_cl

FULL_INVENTORY = {}


def main_menu(user_prompt=None):
    """Provide the user with an input interface."""
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options) - 1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

# def getPrice(itemCode):
#     print("Get price")


def add_new_item():
    """Add new item to FULL_INVENTORY, based on item type and attributes."""
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")
    # Get price from the market prices module
    item_price = mkt_prc.get_latest_price(item_code)
    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = \
        furn_cl.Furniture(item_code, item_description, item_price, item_rental_price,
                          item_material, item_size)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = \
            el_app_cl.ElectricAppliances(item_code, item_description, item_price,
                                         item_rental_price, item_brand, item_voltage)
        else:
            new_item = \
            inven_cl.Inventory(item_code, item_description, item_price, item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_data_struct()
    print("New inventory item added")
    return new_item


def item_info():
    """Retrieve item information, or inform the user that it is not found."""
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for i, k in print_dict.items():
            print("{}:{}".format(i, k))
    else:
        print("Item not found in inventory")


def exit_program():
    """Exit the program."""
    sys.exit()


if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
