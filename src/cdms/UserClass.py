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
        return ["id", "username", "password", "firstname", "lastname"]

    def __str__(self):
        return f"ID: {self.id}\n" \
               f"Username: {self.username} \n" \
               f"Password: {self.password} \n" \
               f"Firstname: {self.firstname} \n" \
               f"Lastname: {self.lastname} \n" \
               f"Registration date: {self.registration_date} \n"
