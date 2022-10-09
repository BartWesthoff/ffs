from datetime import datetime
from src.cdms.InputValidationClass import Validator
from src.cdms.helperClass import Helper


class Member:
    def __init__(self, firstname=None, lastname=None, mail=None, street=None, house_number=None, zipcode=None,
                 city=None,
                 mobile_number=None, registration_date=None, id=None):
        self.firstname = firstname
        self.lastname = lastname
        self.mail = mail
        self.street = street
        self.house_number = house_number
        self.zipcode = zipcode
        self.city = city
        self.mobile_number = mobile_number
        self.registration_date = registration_date
        self.id = id

    @staticmethod
    def create_member():
        from src.cdms.databaseclass import Database
        from src.cdms.userinterfaceClass import UserInterface
        database = Database("analyse.db")

        firstname = Validator().is_valid_name(input("What is your Firstname?: "))
        firstname = Helper().encrypt(firstname)

        lastname = Validator().is_valid_name(input("What is your Lastname?: "))
        lastname = Helper().encrypt(lastname)

        email = Validator().is_valid_email(input("Please enter a email-address: "))
        email = Helper().encrypt(email)

        street = Validator().is_valid_name(input("Please enter a streetname: "))
        street = Helper().encrypt(street)

        house_number = Validator().is_valid_number(input("Please enter a house number: "))
        house_number = Helper().encrypt(house_number)

        zipcode = Validator().is_valid_zipcode(input("Please enter a zipcode: "))
        zipcode = Helper().encrypt(zipcode.upper())

        list_of_cities = ["Rotterdam", "Amsterdam", "Alkmaar", "Maastricht", "Utrecht", "Almere", "Lelystad",
                          "Maassluis",
                          "Vlaardingen", "Schiedam"]
        city_index = UserInterface().choices(choices=list_of_cities, question="Please select a city: ")

        city = Helper().encrypt(list_of_cities[city_index - 1])
        mobile_number = Validator().is_valid_phone_number(input("Please enter a mobile number (31-6-XXXXXXXX): "))
        mobile_number = "31-6-" + mobile_number
        mobile_number = Helper().encrypt(mobile_number)

        uuid = Helper.generate_uuid()

        member = Member(firstname=firstname, lastname=lastname, mail=email, street=street, house_number=house_number,
                        zipcode=zipcode, city=city, registration_date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        mobile_number=mobile_number,
                        id=uuid)
        database.create_member(member)
        return member

    def search_member(self, search_term):
        for attribute in self.get_attributes():
            if search_term in getattr(self, attribute).lower():
                return True
        return False

    @staticmethod
    def get_attributes():
        return ["firstname", "lastname", "mail", "street", "house_number", "zipcode", "city", "mobile_number"]

    @staticmethod
    def to_member_encrypt(data):
        if type(data) == Member:
            return Member(firstname=Helper().encrypt(data.firstname), lastname=Helper().encrypt(data.lastname),
                          mail=Helper().encrypt(data.mail), street=Helper().encrypt(data.street),
                          house_number=Helper().encrypt(data.house_number), zipcode=Helper().encrypt(data.zipcode),
                          city=Helper().encrypt(data.city), mobile_number=Helper().encrypt(data.mobile_number),
                          registration_date=data.registration_date, id=data.id)
        else:
            return Member(firstname=Helper().encrypt(data[0]), lastname=Helper().encrypt(data[1]),
                          mail=Helper().encrypt(data[2]), street=Helper().encrypt(data[3]),
                          house_number=Helper().encrypt(data[4]), zipcode=Helper().encrypt(data[5]),
                          city=Helper().encrypt(data[6]), mobile_number=Helper().encrypt(data[7]),
                          registration_date=data[8], id=data[9])

    @staticmethod
    def dummy_member():
        firstname = "test"
        lastname = "test"
        mail = "mail"
        street = "street"
        house_number = "house_number"
        zipcode = "zipcode"
        city = "city"
        mobile_number = "mobile_number"
        registration_date = datetime.now().strftime("%d-%m-%Y")
        id = "id"

        return Member(firstname=firstname, lastname=lastname, mail=mail, street=street, house_number=house_number,
                      zipcode=zipcode, city=city, registration_date=registration_date, mobile_number=mobile_number,
                      id=id)

    @staticmethod
    def to_member(data):
        return Member(id=data[0], firstname=data[1], lastname=data[2], street=data[3], house_number=data[4],
                      zipcode=data[5], city=data[6], mail=data[7], mobile_number=data[8], registration_date=data[9],
                      )

    @staticmethod
    def to_member_decrypt(data):
        # TOOD: make generic for data en member (self)
        if type(data) == Member:
            return Member(id=data.id, firstname=Helper().decrypt(data.firstname),
                          lastname=Helper().decrypt(data.lastname),
                          street=Helper().decrypt(data.street), house_number=Helper().decrypt(data.house_number),
                          zipcode=Helper().decrypt(data.zipcode), city=Helper().decrypt(data.city),
                          mail=Helper().decrypt(data.mail), mobile_number=Helper().decrypt(data.mobile_number),
                          registration_date=data.registration_date)
        else:
            return Member(id=data[0], firstname=Helper().decrypt(data[1]), lastname=Helper().decrypt(data[2]),
                          street=Helper().decrypt(data[3]), house_number=Helper().decrypt(data[4]),
                          zipcode=Helper().decrypt(data[5]), city=Helper().decrypt(data[6]),
                          mail=Helper().decrypt(data[7]), mobile_number=Helper().decrypt(data[8]),
                          registration_date=data[9])

    def __str__(self):
        """ dit is to str() methode"""
        return f"Member: \n" \
               f"Id: {self.id}\n" \
               f"Firstname: {self.firstname} \n" \
               f"Lastname: {self.lastname} \n" \
               f"Street: {self.street} \n" \
               f"House number: {self.house_number} \n" \
               f"Zipcode: {self.zipcode} \n" \
               f"City: {self.city} \n" \
               f"Email: {self.mail} \n" \
               f"Mobile number: {self.mobile_number} \n" \
               f"Registration date: {self.registration_date} \n" \
               f""
