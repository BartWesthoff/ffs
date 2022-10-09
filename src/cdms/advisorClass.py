""""
Advisor class
"""
from src.cdms.UserClass import User
from src.cdms.helperClass import Helper


class Advisor(User):

    def __init__(self, username, password, firstname, lastname, uuid, registration_date):
        super().__init__(username, password, firstname, lastname, uuid, registration_date)

    @staticmethod
    def to_advisor(data):
        return Advisor(uuid=data[4], username=data[0], password=data[1], firstname=data[2], lastname=data[3],
                       registration_date=data[5])

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
