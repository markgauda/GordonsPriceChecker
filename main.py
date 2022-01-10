#! python3
"""
This program was made by Mark Gauda in the winter of 2022
This program will check the gordons resturaunt supply store to see
if the prices of items are below a specified price, and if they are,
the user will be notified
"""
import logging
from time import sleep
from EmailHandler import EmailHandler
import Item
import schedule
import time
loggingFormat = "%(asctime)s ~ %(levelname)s ~ %(message)s"
logging.basicConfig(level = logging.DEBUG, format = loggingFormat)

def main():
    schedule.every().day.at("12:00").do(check_the_items)
    while True:
        schedule.run_pending()
        time.sleep(.5)

def check_the_items():
    logging.debug("Starting price tracker Main()")
    item_list = make_list_of_items()
    #loop through each item in the list
    for item in item_list:
        #check the price of the current item
        logging.debug("Checking item with ID: "+ item.id)
        item.update_item() #update price and quantity
        #is the price_now <= price_wanted?
        if(item.price_now <= item.price_wanted and item.price_now != 0.0):
            item.send_notification_email()





def make_item_file(file_name):
    with open(file_name, 'w') as output_file:
        print("enter 'e' to exit")
        while True:
            item_id = input("What is the ID you would like to track=> ")
            if (item_id.lower() == 'e'):
                break
            elif (not item_id.isnumeric):
                print("Please only enter a number or the letter 'e'")
            elif (item_id.isnumeric):
                price_wanted = input("What is the price you would like to set the watch point at=> ")
                price_wanted = price_wanted.strip(" $")
                if (price_wanted.lower() == 'e'):
                    break
                elif (not price_wanted.isnumeric):
                    print("Please only enter a number or the letter 'e'")
                elif (price_wanted.replace('.','').isnumeric): #strip the bad chars
                    print("Adding " + item_id + " to the tracker")
                    output_file.write(item_id+" ")
                    print("Adding " + price_wanted + " to the tracker")
                    output_file.write(price_wanted + '\n')

def make_list_of_items():
    #Try to open the item file, if it dosen't exist, make it
    file_name = "item_objects.txt"
    try:
        logging.debug("Trying to open the item file")
        input_file = open(file_name, "rt")
            

    except:
        logging.debug("there was an error openeing the item file")
        make_item_file(file_name)
        input_file = open(file_name, "rt")

        
    #Make a list of item objects
    item_list = list()
    for line in input_file:
        line_parts = line.split(" ")
        item_id = line_parts[0]
        price_wanted = line_parts[1]
        item_list.append(Item.GordonsItem(item_id, price_wanted))
        
    #Close the item file
    input_file.close()

    return item_list



main()