"""This file was created by Mark Gauda in the winter of 2022
This file is a test driver for the email.py module
"""
import EmailHandler

email_object = EmailHandler.EmailHandler()

print(email_object.connected_to_server)

email_object.send_an_email("This is a test", "Hello from the program!")
