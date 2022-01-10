"""This file was created by Mark Gauda in the winter of 2022
This file is a test driver for the EmailHandler.py module
"""
import EmailHandler

email_object = EmailHandler.EmailHandler()

print(email_object.connected_to_server)

subject = "This is a test"
message = "Hello from the program!"
email_object.send_an_email(subject, message)
