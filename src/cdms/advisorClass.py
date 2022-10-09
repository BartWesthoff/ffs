""""
Advisor class
"""
from cdms.UserClass import User
from cdms.helperClass import Helper


class Advisor(User):

    def __init__(self, username, password, firstname, lastname, registration_date, id):
        super().__init__(username, password, firstname, lastname,  registration_date, id)

    @staticmethod
    def to_advisor(data):
        return Advisor(username=data[0], password=data[1], firstname=data[2], lastname=data[3],
                       registration_date=data[5])


    @staticmethod
    def to_advisor_encrypt(data):
        if type(data) == Advisor:
            return Advisor(id=Helper().encrypt(data.id), username=Helper().encrypt(data.username),
                           password=Helper().encrypt(data.password),
                           firstname=Helper().encrypt(data.firstname), lastname=Helper().encrypt(data.lastname),
                           registration_date=data.registration_date)
        else:
            return Advisor(id=Helper().encrypt(data[0]),
                           password=Helper().encrypt(data[4]), username=Helper().encrypt(data[3]),
                           firstname=Helper().encrypt(data[1]), lastname=Helper().encrypt(data[2]),
                           registration_date=data[5])

    @staticmethod
    def to_advisor_decrypt(data):

        if type(data) == Advisor:
            return Advisor(username=Helper().decrypt(data.username), password=Helper().decrypt(data.password),
                           firstname=Helper().decrypt(data.firstname), lastname=Helper().decrypt(data.lastname),
                           registration_date=data.registration_date, id=data.id)
        else:
            return Advisor(id=Helper().decrypt(data[0]), firstname=Helper().decrypt(data[1]), lastname=Helper().decrypt(data[2]),  username=Helper().decrypt(data[3]) ,password=Helper().decrypt(data[4]),
                           registration_date=data[5])

    def __str__(self):
        """ dit is to str() methode"""
        return f"Advisor: \n" \
               f"ID: {self.id}\n" \
               f"Username: {self.username} \n" \
               f"Firstname: {self.firstname} \n" \
               f"Lastname: {self.lastname} \n" \
               f"Registration date: {self.registration_date} \n"

    def search_advisor(self, search_term):
        return self.search_user(search_term)
