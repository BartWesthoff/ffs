import io
import json
import re
import sqlite3
from tabnanny import check
from turtle import isvisible

from mysqlx import FilterableStatement


class Validator:

    @staticmethod
    def isValidNumber(number):
        if(number.isnumeric() != True):
            return False
        else:
            return True
    
    def isValidName(self, Name):
        # NameStrip = Name.rstrip('\x00')
        if(Name.isnumeric()):
            Name = input("Name cannot be a integer. Try again: ")
            self.isValidName(Name)
        elif(len(Name) > 20):
            Name = input("Name cannot be a longer than 30 characters. Try again: ")
            self.isValidName(Name)
        # elif(NameStrip != Name):
        #     Name = input("Name cannot contain Null Bytes. Try again: ")
        #     self.isValidName(Name)
    
        return Name

