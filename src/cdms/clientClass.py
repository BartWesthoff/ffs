import re
from datetime import datetime
from random import *
from src.cdms.helperClass import Helper


class Client:
    # TODO: Loggen als iets fout wordt ingevoerd.
    def __init__(self, firstname=None, lastname=None, mail=None, street=None, housenumber=None, zipcode=None, city=None,
                 mobile_number=None, registration_date=None, id=None):
        self.firstname = firstname
        self.lastname = lastname
        self.mail = mail
        self.street = street
        self.housenumber = housenumber
        self.zipcode = zipcode
        self.city = city
        self.mobile_number = mobile_number
        self.registration_date = registration_date
        self.id = id

    @staticmethod
    def newClient():
        print("went in new client")
        firstname = input("What is your Firstname?: ")
        lastname = input("What is your Lastname?: ")
        mail = ""
        street = ""
        housenumber = -1
        zipcode = ""
        mobile_number = ""
        firstname = Helper().Encrypt(firstname)
        lastname = Helper().Encrypt(lastname)
        loop = True
        while loop:
            mail = input("What is the email?: ")
            _validEmail = re.search("^[a-zA-Z\d_.+-]+@[a-zA-Z\d-]+\.[a-zA-Z\d-.]+$", mail)
            if _validEmail:
                mail = Helper().Encrypt(mail)
                loop = False
            else:
                print("Email is incorrect, try again.")
        loop = True
        while loop:
            street = input("What is the streetname?: ")
            if street.isalpha():
                street = Helper().Encrypt(street)
                loop = False
            else:
                print("Streetname is incorrect, try again.")
        loop = True
        while loop:
            housenumber = input("What is the house number?: ")
            if housenumber.isnumeric():
                housenumber = Helper().Encrypt(housenumber)
                loop = False
            else:
                print("Housenumber is incorrect, try again.")
        loop = True
        while loop:
            zipcode = input("What is the zipcode?: ").upper()
            if zipcode[0:3].isnumeric() and zipcode[4:5].isalpha() and len(zipcode) == 6:
                loop = False
                zipcode = Helper().Encrypt(zipcode)
            else:
                print("Wrong zipcode, try again.")
        listOfCities = ["Rotterdam", "Amsterdam", "Alkmaar", "Maastricht", "Utrecht", "Almere", "Lelystad", "Maassluis",
                        "Vlaardingen", "Schiedam"]
        index = 1
        while index <= len(listOfCities):
            print(f"{index}. {listOfCities[index - 1]}")
            index += 1
        city = listOfCities[(int(input("In wich city do you live (choose from 1-10)"))) - 1]
        print(city)
        city = Helper().Encrypt(city)
        loop = True
        while loop:
            mobile_number = input("What is your mobile number?:\n31-6-")
            if mobile_number.isnumeric() and len(mobile_number) == 8:
                loop = False
            else:
                print("mobile number is not correct, try again.")

        mobile_number = "31-6-" + mobile_number
        mobile_number = Helper().Encrypt(mobile_number)

        id = [str(randint(0 if i == 0 else 1, 9)) for i in range(9)]
        last_digit = sum(int(i) for i in id) % 10
        id = ''.join(id) + str(last_digit)

        return Client(firstname=firstname, lastname=lastname, mail=mail, street=street, housenumber=housenumber,
                      zipcode=zipcode, city=city, registration_date=datetime.now(), mobile_number=mobile_number, id=id)
