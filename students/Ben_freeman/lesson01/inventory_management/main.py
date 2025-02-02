# Launches the user interface for the inventory management system
"""module docstring"""
import sys
from inventory_management import market_prices
from inventory_management import electric_appliances_class
from inventory_management import furniture_class
from inventory_management import inventory_class


def mainmenu(user_prompt=None):
    """Function docstring"""
    valid_prompts = {"1": addnewitem,
                     "2": iteminfo,
                     "q": exitprogram}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def getprice():
    """function docstring"""
    print("Get price")


def addnewitem():
    """function docstring"""
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = furniture_class.Furniture(
            item_code, item_description, item_price, item_rental_price, item_material, item_size
        )
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = electric_appliances_class.ElectricAppliances(
                item_code, item_description, item_price, item_rental_price, item_brand, item_voltage
            )
        else:
            new_item = inventory_class.Inventory(
                item_code, item_description, item_price, item_rental_price
            )
    FULL_INVENTORY[item_code] = new_item.returnasdictionary()
    print("New inventory item added")


def iteminfo():
    """function docstring"""
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for k, j in print_dict.items():
            print("{}:{}".format(k, j))
    else:
        print("Item not found in inventory")


def exitprogram():
    """function docstring"""
    sys.exit()


if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        mainmenu()()
        input("Press Enter to continue...........")
