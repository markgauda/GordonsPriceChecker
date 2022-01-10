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
    assert testItem.price_now == 0.0, "The item price now was not set to 0.0"
    assert testItem.quantity_in_stock == 0, "The quantity was not set to 0"
    testItem.update_item()
    assert testItem.price_now == 94.99, "The item price was not succesfuly updated (check website to make sure it didn't change)"
    assert testItem.quantity_in_stock == 3, "The quantity was not succesfuly updated (check website to make sure it didn't change)"
    testItem.send_notification_email()

main()