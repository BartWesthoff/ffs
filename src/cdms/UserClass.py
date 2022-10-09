from src.cdms.helperClass import Helper


class User:

    def __init__(self, username, password, firstname, lastname, registration_date, id):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.id = id
        self.registration_date = registration_date

    def search_user(self, search_term):
        for attribute in self.get_attributes():
            if search_term in getattr(self, attribute).lower():
                return True
        return False

    @staticmethod
    def get_attributes():
        return ["username", "password", "firstname", "lastname"]

    def __str__(self):
        return f"ID: {self.id}\n" \
               f"Firstname: {self.firstname} \n" \
               f"Lastname: {self.lastname} \n" \
               f"Username: {self.username} \n" \
               f"Password: {self.password} \n" \
               f"Registration date: {self.registration_date} \n"
    @staticmethod
    def to_user(data):
        return User(id=data[0], username=data[1], password=data[2], firstname=data[3], lastname=data[4],
                    registration_date=data[5])

    @staticmethod
    def to_user_decrypt(data):
        if type(data) == User:
            return User(id=Helper().decrypt(data.id), username=Helper().decrypt(data.username),
                        password=Helper().decrypt(data.password),
                        firstname=Helper().decrypt(data.firstname), lastname=Helper().decrypt(data.lastname),
                        registration_date=data.registration_date)
        else:
            return User(id=Helper().decrypt(data[0]),
                        password=Helper().decrypt(data[4]),username=Helper().decrypt(data[3]),
                        firstname=Helper().decrypt(data[1]), lastname=Helper().decrypt(data[2]),
                        registration_date=data[5])


# TODO: short list goedzetten