""""
Advisor class
"""
from src.cdms.helperClass import Helper


class Advisor:

    def __init__(self, username, password, firstname, lastname, uuid, registration_date):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.registration_date = registration_date
        self.uuid = uuid
        self.attributes = ["username", "password", "firstname", "lastname"]

    @staticmethod
    def to_advisor(data):
        return Advisor(uuid=data[4], username=data[0], password=data[1], firstname=data[2], lastname=data[3],
                       registration_date=data[5])

    def search_advisor(self, search_term):
        for attribute in self.attributes:
            if search_term in getattr(self, attribute).lower():
                return True
        return False

    @staticmethod
    def get_attributes():
        return ["username", "password", "firstname", "lastname"]

    @staticmethod
    def to_advisor_decrypt(data):

        if type(data) == Advisor:
            return Advisor(username=Helper().decrypt(data.username), password=Helper().decrypt(data.password),
                           firstname=Helper().decrypt(data.firstname), lastname=Helper().decrypt(data.lastname),
                           registration_date=data.registration_date, uuid=data.uuid)
        else:
            return Advisor(username=Helper().decrypt(data[0]), password=Helper().decrypt(data[1]),
                           firstname=Helper().decrypt(data[2]), lastname=Helper().decrypt(data[3]),
                           registration_date=data[5], uuid=data[4])


    def __str__(self):
        """ dit is to str() methode"""
        return f"Advisor: \n" \
               f"UUID: {self.uuid}\n" \
               f"Username: {self.username} \n" \
               f"Password: {self.password} \n" \
               f"Firstname: {self.firstname} \n" \
               f"Lastname: {self.lastname} \n" \
               f"Registration date: {self.registration_date} \n"







