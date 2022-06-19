from pdb import lasti2lineno
from src.cdms.memberClass import Member
from src.cdms.databaseclass import Database
from src.cdms.helperClass import Helper
from src.cdms.InputValidationClass import Validator


# database.write(f"Logging", '`username`, `datetime`, `description`, `suspicious`', f"'{firstname}', '{lastname}', '{username}', '{password}'")


class PersonCRUD:

    @staticmethod
    def addPerson(kind):
        database = Database("analyse.db")
        if kind.lower() in ["advisor", "systemadmin"]:
            firstname = input("firstname?: ")
            firstname = Helper().Encrypt(firstname)
            lastname = input("lastname?: ")
            lastname = Helper().Encrypt(lastname)
            username = input("username?:")
            username = Helper().usernameChecker(username)
            username = Helper().Encrypt(username)
            password = input("password?: ")
            password = Helper().passwordchecker(password)
            password = Helper().Encrypt(password)

            database.createEmployee(kind, firstname, lastname, username, password)

        elif kind.lower() == "member":
            # member = Member().dummyMember()  # todo change to real member
            member = Member().createMember()
            database.createMember(member)
        database.commit()
        database.close()

    @staticmethod
    def searchPerson(kind):
        print(kind)
        loop = True
        count = 0
        user = Helper().checkLoggedIn()
        print(user)
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            print(row)
            print("ID          |", row[0])
            print("Firstname   |", Helper().Decrypt(row[1]))
            print("Lastname    |", Helper().Decrypt(row[2]) + "\n")
            
        
        while loop:
            firstname = input("firstname?: ")
            print(firstname)
            firstname = Validator().isValidName(firstname)
            print(firstname)
            firstname = Helper().Encrypt(firstname)

            lastname = input("lastname?: ")
            lastname = Validator().isValidName(lastname)
            print(lastname)

            lastname = Helper().Encrypt(lastname)
            

          
            data = database.searchPerson(kind=kind, firstname=firstname, lastname=lastname)
            database.commit()
            if data is not None:

                member = Member().toMember(data)

                print("ID            |", member.id)
                print("Firstname     |", Helper.Decrypt(member.firstname))
                print("Lastname      |", Helper.Decrypt(member.lastname))
                print("Street        |", Helper.Decrypt(member.street))
                print("Housenumber   |", Helper.Decrypt(member.housenumber))
                print("Zipcode       |", Helper.Decrypt(member.zipcode))
                print("City          |", Helper.Decrypt(member.city))
                print("mail          |", Helper.Decrypt(member.mail))
                print("Phone         |", Helper.Decrypt(member.mobile_number))
                print("creation date |", member.registration_date)

                loop = False
            elif data is None:
                print("Member not found, try again.")

        database.close()

    @staticmethod
    def deletePerson(kind):
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            print(row)
            print("ID          |", row[0])
            print("Firstname   |", Helper().Decrypt(row[1]))
            print("Lastname    |", Helper().Decrypt(row[2]))
            print(f"Role        | {kind}\n")
        
        firstname = input("firstname?: ")
        firstname = Validator().isValidName(firstname)

        lastname = input("lastname?: ")
        lastname = Validator().isValidName(lastname)

        firstname = Helper().Encrypt(firstname)
        lastname = Helper().Encrypt(lastname)

        data = database.searchPerson(kind=kind,firstname=firstname, lastname=lastname)
        if data is not None:
            # database.query(f"DELETE FROM "systemadmin" WHERE 'firstname'='{firstname}' AND 'lastname'='{lastname}'")
            database.deletePerson(table=kind, firstname=firstname, lastname=lastname)
            database.commit()
            print("Deleted")
        else:
            print("Person not found, Try again.\n")

    def modifyPerson(self, kind):
        from src.cdms.userinterfaceClass import userinterface
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        print(data)
        for row in data:
            print(row)
            print("ID          |", row[0])
            print("Firstname   |", Helper().Decrypt(row[1]))
            print("Lastname    |", Helper().Decrypt(row[2]))
            print(f"Role        | {kind}\n")

        _firstname = input(f"What is the firstname of the {kind}?: ")
        _firstname = Validator().isValidName(_firstname)

        _lastname = input(f"What is the lastname of the {kind}?: ")
        _lastname = Validator().isValidName(_lastname)

        _firstname = Helper().Encrypt(_firstname)
        _lastname = Helper().Encrypt(_lastname)
        data = database.searchPerson(kind=kind, firstname=_firstname, lastname=_lastname)
        if data is None:
            print("Member not found, try again.")
            self.modifyPerson(kind)
        attr = ["firstname", "lastname", "streetname", "housenumber", "zipcode", "city", "emailaddress", "mobilephone"]
        choices = []
        for att in attr:
            choices.append(f"Modify {att}")
        choice = userinterface().choices(choices)

        new_data = input(f"What will be the new {attr[choice - 1]}: ")
        for x in attr:
            if(choice == 1 or choice == 2):
                new_data = Validator().isValidName(new_data)
            elif(choice == 3):
                new_data = Validator().isValidStreetname(new_data)
            elif(choice == 4):
                new_data = Validator().isValidNumber(new_data)
            elif(choice == 5):
                new_data = Validator().isValidZipcode(new_data)
            elif(choice == 6):
                new_data = Validator().isValidZipcode(new_data)
            elif(choice == 7):
                new_data = Validator().isValidEmail(new_data)
            elif(choice == 8):
                new_data = Validator().isValidEmail(new_data)
            




        new_data = Helper().Encrypt(new_data)
        database.query(
            f"UPDATE {kind} SET {attr[choice - 1]} = ? WHERE firstname = ? AND lastname = ?;",
            (new_data, _firstname, _lastname))
        database.commit()
        database.close()

    @staticmethod
    def changePassword(kind):

        database = Database("analyse.db")
        from src.cdms.userinterfaceClass import userinterface
        choice = userinterface().choices(
            ["Reset own password.", "Reset an advisors password.", "Reset an systemadmin password"])
        kind_target = ""
        if choice == 2:
            kind_target = 'advisor'
        elif choice == 3:
            kind_target = 'systemadmin'
        username_target = None
        Hastarget = choice in [2, 3]
        if Hastarget:
            data = database.getAllofKind(kind=f"{'advisor' if choice == 2 else 'systemadmin'}")
            if data is not None:
                for enity in data:
                    print(enity)
                    print("id                | ", enity[0])
                    print("firstname         | ", Helper.Decrypt(enity[1]))
                    print("lastname          | ", Helper.Decrypt(enity[2]))
                    print("username          | ", Helper.Decrypt(enity[3]))
                    print("password          | ", Helper.Decrypt(enity[4]))

                username_target = input(f"What is the username of the {'advisor' if choice == 2 else 'system admin'}: ")
                username_target = Helper().Encrypt(username_target)
        username_user = Helper().checkLoggedIn()
        print(username_user)

        username_user = Helper().Decrypt(username_user)

        _password = input(
            "What will be ur password? Min length of 8, no longer than 30 characters, MUST have at least one "
            "lowercase letter, one uppercase letter, one digit and one special character : ")
        password = Helper().passwordchecker(password=_password)  # TODO check this function
        password = Helper().Encrypt(password)
        username_to_change = username_user if choice == 1 else username_target
        print(username_to_change)
        print(password)

        database.updatePassword(kind=kind_target, username=username_to_change, password=password)

        database.commit()
        database.close()

    @staticmethod
    def checkUsers():
        # kind kunnen we hier gebruiken?
        from src.cdms.userinterfaceClass import userinterface
        loop = True
        database = Database("analyse.db")
        while loop:
            choice = userinterface().choices(
                ["Check Advisors", "Check System Administrators",
                 "Check Super Administrator"])  # TODO check regular memebers
            _type = None
            if choice == 1:
                _type = "advisor"
            elif choice == 2:
                _type = "systemadmin"
            elif choice == 3:
                _type = "superadmin"
            else:
                print("Incorrect input, try again.")

            print(f'\n{_type}: \n')
            data = database.get(columns='*', table=_type)
            for row in data:
                print(row)
                print("ID          |", row[0])
                print("Firstname   |", Helper().Decrypt(row[1]))
                print("Lastname    |", Helper().Decrypt(row[2]))
                print("Username    |", Helper().Decrypt(row[3]))
                print(f"Role        | {_type}\n")
            loop = False

        database.close()
