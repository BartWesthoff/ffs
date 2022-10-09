from cdms.UserClass import User
from cdms.helperClass import Helper


class SystemAdmin(User):

    def __int__(self, username, password, firstname, lastname, registration_date, id):
        super().__init__(username, password, firstname, lastname, registration_date, id)

    def __str__(self):
        return f"SystemAdmin: \n" \
               f"Username: {self.username} \n" \
               f"Password: {self.password} \n" \
               f"Firstname: {self.firstname} \n" \
               f"Lastname: {self.lastname} \n" \
               f"Registration date: {self.registration_date} \n"

    @staticmethod
    def to_system_admin(data):
        return SystemAdmin(id=data[4], username=data[0], password=data[1], firstname=data[2], lastname=data[3],
                           registration_date=data[5])

    @staticmethod
    def to_system_admin_decrypt(data):

        if type(data) == SystemAdmin:
            return SystemAdmin(username=Helper().decrypt(data.username), password=Helper().decrypt(data.password),
                               firstname=Helper().decrypt(data.firstname), lastname=Helper().decrypt(data.lastname),
                               registration_date=data.registration_date, id=data.id)
        else:
            return SystemAdmin(username=Helper().decrypt(data[0]), password=Helper().decrypt(data[1]),
                               firstname=Helper().decrypt(data[2]), lastname=Helper().decrypt(data[3]),
                               registration_date=data[5], id=data[4])
