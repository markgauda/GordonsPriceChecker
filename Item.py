"""
This was created by Mark Gauda in the winter of 2022
This is the class for a gordons Item

Todo: consider generalizing the Item class so you can make
    a tracker for multiple websites
"""
import logging
import requests
from bs4 import BeautifulSoup
from EmailHandler import EmailHandler
loggingFormat = "%(asctime)s ~ %(levelname)s ~ %(message)s"
logging.basicConfig(level = logging.DEBUG, format = loggingFormat)


class GordonsItem():
    def __init__(self, item_id, price_wanted):
        self.id = item_id
        self.price_wanted = float(price_wanted)
        self.item_url = "https://www.gordonrestaurantmarket.com/products/" + str(item_id) + '/' 
        self.price_now = 0.0
        self.quantity_in_stock = 0

    def update_item(self):
        website_soup = self.get_website_soup()
        price = self.look_for_price_on_page(website_soup)
        quantity = self.look_for_quantity_on_page(website_soup)
        if (price != None):
            self.price_now = float(price)
        if (quantity != None):
            self.quantity_in_stock = int(quantity)


    def get_website_soup(self):
        #connect to the gordons site
        website_request = self.connect_to_URL()
        if(website_request == None):
            return None
        #make BS object
        website_soup = self.make_beautiful_soup_object(website_request)
        #return soup
        return website_soup

        

    def connect_to_URL(self):
        """
        This method will try to connect to the gordons site
        If the connection is successful, this will return the
        request object
        If the connection is unsuccessful, this will return None
        """
        #Make the Item URL
        item_url = self.item_url
        try:
            #Request data from the gordons website
            website_data = requests.get(item_url)

        except:
            log_message = "could not connect to url with item id "+\
                str(self.id)
            logging.info(log_message)
            return None
        
        try:
            
            #check to make sure the URL gave good info
            website_data.raise_for_status()
        except:
            log_message ="failed connect to URL with status code "+\
                str(website_data.status_code)
            logging.info(log_message)
            return None
        return website_data

    def make_beautiful_soup_object(self, website_request):
        """This function will make a beautiful soup object out of HTML

        Args:
            website_request (String): The HTML to turn into a soup object
        """
        website_soup = BeautifulSoup(website_request.text, "html.parser")
        return website_soup


    def look_for_price_on_page(self, website_soup):
        """This will look through the soup to find the current

        Args:
            website_soup (BeautifulSoup): This is the website html as a
            beautiful soup object
        
        Return:
            The price of the item on that webpage or None if no price is found
        """
        website_unit_price = website_soup.find_all("span", class_ = "unit_price", limit = 1)
        try:
            unit_price = website_unit_price[0].text #Get the numbers
        except:
            logging.info("There was no price found on this page")
            return None
        unit_price = unit_price.strip(" $") #Get that formating out of there
        return unit_price
    
    def look_for_quantity_on_page(self, website_soup):
        """This function will look through the website soup and find the quantity of the product

        Args:
            website_soup (BeautifulSoup): This is the HTML that has been parsed and turned into a BS object

        Returns:
            Int: The quantity of the item
            None: If there is an error and no quantity can be found
        """
        website_quantity = website_soup.find_all("span", class_ = "item_inventory_stock_level", limit = 1)
        try:
            quantity = website_quantity[0]. text

        except:
            logging.info("There was no quantity found on the page")
            return None
        return quantity
        

    def send_notification_email(self):
        """This function will send an email notifictation for this item
        """
        price = str(self.price_now)
        url = str(self.item_url)
        quantity = str(self.quantity_in_stock)
        item_id = str(self.id)
        email_handler = EmailHandler()
        email_message = "\nThe item with the ID: " + item_id +\
            " is on sale right now for $" + price +\
            " and there are " + quantity + " left in stock." +\
            "\nTo buy this item, click " + "here: " + url
        email_subject = "There is a sale on Gordons item " + item_id
        email_handler.send_an_email(email_subject, email_message)
        
