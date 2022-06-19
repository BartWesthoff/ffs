import io
import json
import re
import sqlite3
from tabnanny import check
from turtle import isvisible

from mysqlx import FilterableStatement


class Validator:

    
    def isValidNumber(self, number):
        if(number.isnumeric() != True):
            number = int(input("Must be a number, try again."))
            self.isValidNumber(number)
        return number
    
    def isValidZipcode(self, zipcode):
        if zipcode[0:3].isnumeric():
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.isValidZipcode(zipcode)
        elif zipcode[4:5].isalpha():
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.isValidZipcode(zipcode)
        elif  len(zipcode) != 6:
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.isValidZipcode(zipcode)
        return zipcode

    def isValidName(self, Name):
        # NameStrip = Name.rstrip('\x00')
        if(Name.isnumeric()):
            Name = input("Name cannot be a integer. Try again: ")
            self.isValidName(Name)
        elif(len(Name) > 20):
            Name = input("Name cannot be a longer than 20 characters. Try again: ")
            self.isValidName(Name)
        # elif(NameStrip != Name):
        #     Name = input("Name cannot contain Null Bytes. Try again: ")
        #     self.isValidName(Name)
    
        return Name

    def isValidStreetname(self, Name):
        # NameStrip = Name.rstrip('\x00')
        if(Name.isalpha() == False):
            Name = input("streetname cannot contain an integer. Try again: ")
            self.isValidStreetname(Name)
        elif(len(Name) > 20):
            Name = input("Name cannot be a longer than 20 characters. Try again: ")
            self.isValidStreetname(Name)
        # elif(NameStrip != Name):
        #     Name = input("Name cannot contain Null Bytes. Try again: ")
        #     self.isValidName(Name)
    
        return Name

    def isValidEmail(self, email):
        validEmail = re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
        if validEmail == False:
            email = input("Please enter a valid email.")
            self.isValidEmail(email)
        return email

    def isValidEmail(self, email):
        validEmail = re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
        if validEmail == False:
            email = input("Please enter a valid email.")
            self.isValidEmail(email)
        return email

    def isValidTelefone(self, number):
        if number.isnumeric() == False:
            number = input("Please enter a valid number")
            self.isValidTelefone(number)
        elif len(number) != 8:
            number = input("Please enter a valid number")
            self.isValidTelefone(number)
        return number