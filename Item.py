"""
This was created by Mark Gauda in the winter of 2022
This is the class for a gordons Item
"""
import logging
import requests
from bs4 import BeautifulSoup
loggingFormat = "%(asctime)s ~ %(levelname)s ~ %(message)s"
logging.basicConfig(level = logging.DEBUG, format = loggingFormat)


class GordonsItem():
    def __init__(self, item_id, price_wanted):
        self.id = item_id
        self.price_wanted = float(price_wanted)
        self.gordons_url = "https://www.gordonrestaurantmarket.com/products/"
        self.price_now = None

    def check_price(self):
        """
        This method will check gordons website to get the price_now
        If there is an error, this will return None
        If there is not an errror, this will return the current price
        of the item
        """
        #connect to the gordons site
        website_request = self.connect_to_URL()
        if(website_request == None):
            return None
        #make BS object
        website_soup = self.make_beautiful_soup_object(website_request)
        #look for price on page
        price = self.look_for_price_on_page(website_soup)
        #return price
        return price

        
        
        

    def connect_to_URL(self):
        """
        This method will try to connect to the gordons site
        If the connection is successful, this will return the
        request object
        If the connection is unsuccessful, this will return None
        """
        #Make the Item URL
        item_url = self.gordons_url + self.item_id + '/'
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
            log_message ="failed connect to URL with status code"+\
                str(website_data.status_code)
            logging.info(log_message)
            return None
        return website_data

    def make_beautiful_soup_object(self, website_request):
        """This function will make a beautiful soup object out of HTML

        Args:
            website_request (String): The HTML to turn into a soup object
        """
        return BeautifulSoup(website_request, "html.parser")


    def look_for_price_on_page(self, website_soup):
        """This will look through the soup to find the current

        Args:
            website_soup (BeautifulSoup): This is the website html as a
            beautiful soup object
        
        Return:
            The price of the item on that webpage
        """
        website_unit_price = website_soup.find_all("span", class_ = "unit_price", limit = 1)
        return website_unit_price[0]
    
        
        
        
