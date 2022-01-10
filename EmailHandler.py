"""This was creaded by Mark Gauda in the winter of 2022
This program will handle the email sending and recieving
This program is made to use the gmail smtp client using tls
"""
import smtplib #the library that handles smtp
import logging
loggingFormat = "%(asctime)s ~ %(levelname)s ~ %(message)s"
logging.basicConfig(level = logging.DEBUG, format = loggingFormat)

class EmailHandler():
    def __init__(self):
        self.login_file = "login_file.txt" #this is where your login info is stored
        credentials = self.get_login_from_file() #Get your email and password from that file
        self.email_addr = credentials[0]
        self.email_pass = credentials[1]
        self.contacts_file = "contact_list.txt"
        self.contacts = self.get_contacts()
        self.smtp_connection = self.connect_to_smtp_server()
        self.connected_to_server = self.start_tls_connection()


    def get_login_from_file(self):
        """This will get your email and password from the file provided in login_file
        The format must be Email on the first line, with a new line, then password on
        the second line
        """
        with open(self.login_file, "rt") as input_file:
            email_addr = input_file.readline()[0:-1] #get rid of the \n
            email_pass = input_file.readline()
        return (email_addr, email_pass)

    def get_contacts(self):
        """This function will look in the contatcts_list file and return a list of
        all the email addresses if each email is stored on a new line, and properly
        formated
        """
        contacts = list()
        with open(self.contacts_file) as input_file:
            for line in input_file:
                contacts.append(line)
        return contacts

    def connect_to_smtp_server(self):
        """This will connect to the google SMTP server and
        Return: an object of that connection
            will return none if there is an error
        """
        port_number = 587
        try:
            logging.debug("Trying to connect to google SMTP server")
            connection = smtplib.SMTP("smtp.gmail.com", port_number)

        
        except:
            logging.info("Could not connect to the google SMTP server via port " + port_number)
            return None
        
        return connection
        
    def start_tls_connection(self):
        """This function will be the main driver for the TLS
        connection to the google mail server
        Returns: True if the connection is successful
                False otherwise
        """
        if(self.connect_to_smtp_server != None):
            log_message = "Starting the TLS connection to SMTP server"
            logging.debug(log_message)
            #send hello message
            
            hello_connection = self.smtp_connection.ehlo()
            if (hello_connection[0] != 250):
                log_message = "The SMTP greeting failed with code "+\
                    hello_connection[0]
                logging.info(log_message)
                return False
            
            #Start TLS encryption
            
            server_status = self.smtp_connection.starttls()
            if (server_status[0] != 220):
                log_message = "The server could not establish a TLS connection, "+\
                    "the error code is: " + server_status[0]
                logging.info(log_message)
                return False
            
            #log in to the server
            try:
                loging_status = self.smtp_connection.login(self.email_addr, self.email_pass)
                if (loging_status[0] != 235):
                    log_message = "The server could not accept your email address or password, "+\
                        "the error code is: " + loging_status[0]
                    logging.info(log_message)
                    return False
            except smtplib.SMTPAuthenticationError:
                log_message = "The login to the SMTP server failed. The email or password could have been"+\
                    " wrong, or make sure that google security allows 'less secure apps'"
                logging.critical(log_message)
            
            log_message = "Successfuly connected and logged into SMTP server"
            logging.debug(log_message)
            return True

        else:
            log_message = "Could not start TLS connection "+\
                "because there is no connection to a smtp server"
            logging.info(log_message)
            return False

    def send_an_email(self, subject,  message):
        """This function will let you send an email to your contact list

        Args:
            subject (String): This is the subject of the email
            message (String): This is the email you are going to send out
        """
        log_message = "Starting to send an email"
        logging.debug(log_message)
        if (not subject.endswith("\n")):
            subject = subject + "\n"
        if (not subject.startswith("Subject:")):
            subject = "Subject: " + subject
        full_message_to_send = subject + message
        for recipient_email in self.contacts:
            try:
                self.smtp_connection.sendmail(self.email_addr, recipient_email, (full_message_to_send))
                logging.debug("Email sent!")

            except:
                log_message = "Could not send an email to " + recipient_email
                logging.info(log_message)



