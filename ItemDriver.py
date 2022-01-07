"""
This file was made by Mark Gauda in the winter of 2022
This file will test the Item.py file to make sure everything
is running smooth
"""

import Item

def main():
    testItem = Item.GordonsItem(477970, 100)
    assert testItem.price_wanted == 100, "The price wanted was not set to 100"
    assert testItem.id == 477970, "The item ID was not set to 477970"
    assert testItem.price_now == None, "The item price now was not set to None"
    testItem.update_price_now()
    assert testItem.price_now == 93.99, "The item price was not succesfuly updated"

main()