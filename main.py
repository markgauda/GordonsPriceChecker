#! python3
"""
This program was made by Mark Gauda in the winter of 2022
This program will check the gordons resturaunt supply store to see
if the prices of items are below a specified price, and if they are,
the user will be notified
"""
import logging
from time import sleep
import Item
loggingFormat = "%(asctime)s ~ %(levelname)s ~ %(message)s"
logging.basicConfig(level = logging.DEBUG, format = loggingFormat)

def main():
    #Try to open the item file, if it dosen't exist, make it
    logging.debug("Starting price tracker Main()")
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
    #loop through each item in the list
    while True:
        for item in item_list:
            #check the price of the current item
            item.update_price_now()
            #is the price_now <= price_wanted?
            if(item.price_now <= item.price_wanted and item.price_now != 0.0):
                #Notify the user
                pass
        sleep(5)

    return None #Dummy return


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



main()