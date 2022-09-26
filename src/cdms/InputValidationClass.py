import re


class Validator:

    def __init__(self):
        pass

    def is_valid_number(self, number):
        if not number.isnumeric():
            number = input("Must be a number, try again.")
            self.is_valid_number(number)
        return int(number)

    def is_valid_zipcode(self, zipcode):
        if not zipcode[0:3].isnumeric():
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.is_valid_zipcode(zipcode)
        if not zipcode[4:5].isalpha():
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.is_valid_zipcode(zipcode)
        if len(zipcode) != 6:
            zipcode = input("Please enter a valid zipcode, try again: ")
            self.is_valid_zipcode(zipcode)
        return zipcode

    def is_valid_name(self, name):
        if name.isnumeric():
            name = input("name cannot be a integer. Try again: ")
            self.is_valid_name(name)
        if len(name) > 20:
            name = input("name cannot be a longer than 20 characters. Try again: ")
            self.is_valid_name(name)

        return name

    def is_valid_streetname(self, name):
        if not name.isalpha():
            name = input("streetname cannot contain an integer. Try again: ")
            self.is_valid_streetname(name)
        if len(name) > 20:
            name = input("name cannot be a longer than 20 characters. Try again: ")
            self.is_valid_streetname(name)

        return name

    def is_valid_email(self, email):
        valid_email = re.search("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
        if not valid_email:
            email = input("Please enter a valid email.")
            self.is_valid_email(email)
        return email

    def is_valid_telephone_number(self, number):
        if not number.isnumeric() or len(number) != 8:
            number = input("Please enter a valid number")
            self.is_valid_telephone_number(number)
        return number
