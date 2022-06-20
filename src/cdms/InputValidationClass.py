import io
import json
import re
import sqlite3


class Validator:

    def isValidNumber(self, number):
        if not number.isnumeric():
            number = input("Must be a number, try again.")
            self.isValidNumber(number)
        return int(number)

    def isValidZipcode(self, zipcode):
        if not zipcode[0:3].isnumeric():
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.isValidZipcode(zipcode)
        if not zipcode[4:5].isalpha():
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.isValidZipcode(zipcode)
        if len(zipcode) != 6:
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.isValidZipcode(zipcode)
        return zipcode

    def isValidname(self, name):
        if name.isnumeric():
            name = input("name cannot be a integer. Try again: ")
            self.isValidname(name)
        if len(name) > 20:
            name = input("name cannot be a longer than 20 characters. Try again: ")
            self.isValidname(name)

        return name

    def isValidStreetname(self, name):
        if not name.isalpha():
            name = input("streetname cannot contain an integer. Try again: ")
            self.isValidStreetname(name)
        if len(name) > 20:
            name = input("name cannot be a longer than 20 characters. Try again: ")
            self.isValidStreetname(name)

        return name

    def isValidEmail(self, email):
        validEmail = re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
        if not validEmail:
            email = input("Please enter a valid email.")
            self.isValidEmail(email)
        return email

    def isValidTelefone(self, number):
        if not number.isnumeric() or len(number) != 8:
            number = input("Please enter a valid number")
            self.isValidTelefone(number)
        return number
