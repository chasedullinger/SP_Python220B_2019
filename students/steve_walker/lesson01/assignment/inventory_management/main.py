"""Launches the user interface for the inventory management system"""

import sys
sys.path.append('../')

import inventory_management.market_prices as market_prices
import inventory_management.inventory_class as inventory
import inventory_management.furniture_class as furniture
import inventory_management.electric_appliances_class as elec


full_inventory = {} # pylint: disable=invalid-name

def main_menu(user_prompt=None):
    """Main menu"""

    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")

    return valid_prompts.get(user_prompt)


# def get_price(item_code): # pylint: disable=unused-argument
#    """Get current market price"""
#
#    print("Get price")


def add_new_item():
    """Add new item to full_inventory"""

    # Consider passing as argument
    global full_inventory # pylint: disable=global-statement, invalid-name

    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")

    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = furniture.Furniture(item_code, item_description,
                                       item_price, item_rental_price,
                                       item_material, item_size)

    else:
        is_electric_appliance = input("Is this item an electric appliance?"
                                      " (Y/N): ")

        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = elec.ElectricAppliances(item_code, item_description,
                                               item_price, item_rental_price,
                                               item_brand, item_voltage)

        else:
            new_item = inventory.Inventory(item_code, item_description,
                                           item_price, item_rental_price)

    full_inventory[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """Return item info from inventory dict"""

    item_code = input("Enter item code: ")

    if item_code in full_inventory:
        print_dict = full_inventory[item_code]
        for k, v in print_dict.items():
            print("{}:{}".format(k, v))

    else:
        print("Item not found in inventory")


def exit_program():
    """Exit program"""

    sys.exit()


if __name__ == '__main__':
    while True:
        print(full_inventory)
        main_menu()()
        input("Press Enter to continue...........")
