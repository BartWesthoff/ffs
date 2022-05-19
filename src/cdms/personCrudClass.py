from src.cdms.clientClass import Client
from src.cdms.databaseclass import Database
from src.cdms.helperClass import Helper


# database.write(f"Logging", '`username`, `datetime`, `description`, `suspicious`', f"'{firstname}', '{lastname}', '{username}', '{password}'")


class PersonCRUD:

    def addPerson(self, kind):
        database = Database("analyse.db")
        if kind.lower() in ["advisors", "systemadmins"]:
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
            # firstname = "BartAdvisor"
            # lastname = "WesthoffAdvisor"
            # username = "BartWAdvisor"
            # password = "Analyse2022!"
            database.createAdvisor(firstname=firstname, lastname=lastname, username=username, password=password)



        elif kind.lower() == "clients":
            client = Client().newClient()
            database.write(f'Clients',
                           '`firstname`, `lastname`, `streetname`, `housenumber`, `zipcode`, `city`, `emailaddress`, '
                           '`mobilephone`',
                           f"'{client.firstname}', '{client.lastname}', '{client.street}', '{client.housenumber}', '{client.zipcode}', '{client.city}', '{client.mail}', '{client.mobile_number}'")

        database.commit()
        database.close()

    def searchPerson(self, kind):
        loop = True
        count = 0
        user = Helper().checkLoggedIn()
        print(user)
        database = Database("analyse.db")
        while loop:

            firstname = input("firstname?: ")
            firstname = Helper().Encrypt(firstname)

            lastname = input("lastname?: ")
            lastname = Helper().Encrypt(lastname)
            data = database.get(columns='*', table=f'{kind}',
                                where=f"`firstname`='{firstname}' AND `lastname`='{lastname}'")
            database.commit()
            try:
                for row in data:
                    print("ID          |", row[0])
                    print("Firstname   |", Helper().Decrypt(row[1]))
                    print("Lastname    |", Helper().Decrypt(row[2]))
                    print("Streetname  |", Helper().Decrypt(row[3]))
                    print("Housenumber |", row[4])
                    print("Zipcode     |", str(Helper().Decrypt(row[5])))
                    print("City        |", Helper().Decrypt(row[6]))
                    print("Email       |", Helper().Decrypt(row[7]))
                    print("Mobilephone |", row[8]), "\n"
                    loop = False

            except:
                print("Person not found, try again. excpet")

        database.close()

    def deletePerson(self, kind):
        database = Database("analyse.db")
        firstname = input("firstname?: ")

        lastname = input("lastname?: ")
        firstname = Helper().Encrypt(firstname)
        lastname = Helper().Encrypt(lastname)
        print(firstname)
        print(lastname)
        try:
            data = database.get(columns='*', table=f'{kind}',
                                where=f"`firstname`='{firstname}' AND `lastname`='{lastname}'")
            print(data)
            # database.query(f"DELETE FROM 'SystemAdmins' WHERE 'firstname'='{firstname}' AND 'lastname'='{lastname}'")
            database.query(f"DELETE FROM '{kind}' WHERE firstname='{firstname}' AND lastname='{lastname}'")
            database.commit()

            print("Deleted")

        except:
            print("not deleted")

    def modifyPerson(self, kind):
        from src.cdms.userinterfaceClass import userinterface
        database = Database("analyse.db")
        _firstname = input(f"What is the firstname of the {kind[:-1]}?: ")
        _lastname = input(f"What is the lastname of the {kind[:-1]}?: ")
        _firstname = Helper().Encrypt(_firstname)
        _lastname = Helper().Encrypt(_lastname)
        data = database.get(columns='*', table=f'{kind}',
                            where=f"`firstname`='{_firstname}' AND `lastname`='{_lastname}'")
        for row in data:
            if row[1] != _firstname and row[2] != _lastname:
                print("Client not found, try again.")
                PersonCRUD.modifyPerson(self, kind)
        attr = ["firstname", "lastname", "username"]
        choices = []
        for att in attr:
            choices.append(f"Modify {att}")
        choice = userinterface().choices(choices, "Wich option do you want to choose?: ")

        new_data = input(f"What will be the new {attr[choice - 1]}")
        new_data = Helper().Encrypt(new_data)
        database.query(
            f"UPDATE {kind} SET {attr[choice - 1]} = '{new_data}' WHERE firstname = '{_firstname}' AND lastname = '{_lastname}';")
        database.commit()
        database.close()

    def changePassword(self, kind):

        database = Database("analyse.db")
        from src.cdms.userinterfaceClass import userinterface
        # _checkPW = Helper().usernameChecker(_password)
        # TODO: niels even kijken
        #    if _checkPW == 0:
        if kind == "Advisors":
            username = Helper().checkLoggedIn()
            print(username)
            username = Helper().Decrypt(username)
            print(username)
            username = Helper().Encrypt(username)

            _password = input("What will be ur password? Min length of 5, max length of 20, MUST start with a letter: ")
            password = Helper().passwordchecker  # TODO check this function
            _password = Helper().Encrypt(_password)
            database.query(f"UPDATE {kind} SET password = '{_password}' WHERE username = '{username}';")
            database.commit()
            database.close()

        if kind == "SuperAdmin":
            choice = userinterface().choices(
                ["Reset own password.", "Reset an advisors password.", "Reset an systemadmin password"],
                "Wich option do you want to choose?: ")
            if choice == 1:
                username = Helper().checkLoggedIn()
                username = Helper().Decrypt(username)
                username = Helper().Encrypt(username)
                _password = input(
                    "What will be ur password? Min length of 8, no longer than 30 characters, MUST have at least one lowercase letter, one uppercase letter, one digit and one special character : ")
                password = Helper().passwordchecker  # TODO check this function
                _password = Helper().Encrypt(_password)
                database.query(f"UPDATE {kind} SET password = '{_password}' WHERE username = '{username}';")
                database.commit()
                database.close()
            elif choice == 2:
                loop = True
                count = 0
                user = Helper().checkLoggedIn()
                database = Database("analyse.db")
                while loop:
                    data = database.get(columns='*', table=f'{"Advisors"}')

                    database.commit()
                    try:
                        for row in data:
                            print("ID          |", row[0])
                            print("Firstname   |", Helper().Decrypt(row[1]))
                            print("Lastname    |", Helper().Decrypt(row[2]))
                            print("Username    |", Helper().Decrypt(row[3])), "\n"
                            loop = False

                    except:
                        print("Person not found, try again. excpet")
                try:

                    username = input("What is the username of the advisor: ")

                    username = Helper().Encrypt(username)
                    _password = input(
                        "What will be ur password? Min length of 8, no longer than 30 characters, MUST have at least one lowercase letter, one uppercase letter, one digit and one special character :")
                    password = Helper().passwordchecker  # TODO check this function
                    kind = "Advisors"
                    _password = Helper().Encrypt(_password)
                    database.query(f"UPDATE {kind} SET password = '{_password}' WHERE username = '{username}';")
                    database.commit()
                    database.close()
                except:
                    print("Person not found. Try again.")

            elif choice == 3:
                loop = True
                count = 0
                user = Helper().checkLoggedIn()
                database = Database("analyse.db")
                while loop:
                    data = database.get(columns='*', table=f'{"SystemAdmins"}')

                    database.commit()
                    try:
                        for row in data:
                            print("ID          |", row[0])
                            print("Firstname   |", Helper().Decrypt(row[1]))
                            print("Lastname    |", Helper().Decrypt(row[2]))
                            print("Username    |", Helper().Decrypt(row[3])), "\n"
                            loop = False

                    except:
                        print("Person not found, try again. excpet")
                try:

                    username = input("What is the username of the advisor: ")

                    username = Helper().Encrypt(username)
                    _password = input(
                        "What will be ur password? Min length of 8, no longer than 30 characters, MUST have at least one lowercase letter, one uppercase letter, one digit and one special character :")
                    password = Helper().passwordchecker  # TODO check this function
                    kind1 = "SystemAdmins"
                    _password = Helper().Encrypt(_password)
                    database.query(f"UPDATE {kind1} SET password = '{_password}' WHERE username = '{username}';")
                    database.commit()
                    database.close()
                except:
                    print("Person not found. Try again.")

        if kind == "SystemAdmins":
            choice = userinterface().choices(
                ["Reset own password.", "Reset an advisors password."],
                "Wich option do you want to choose?: ")
            if choice == 1:
                username = Helper().checkLoggedIn()
                username = Helper().Decrypt(username)
                username = Helper().Encrypt(username)
                _password = input(
                    "What will be ur password? Min length of 8, no longer than 30 characters, MUST have at least one lowercase letter, one uppercase letter, one digit and one special character : ")
                password = Helper().passwordchecker  # TODO check this function
                _password = Helper().Encrypt(_password)
                database.query(f"UPDATE {kind} SET password = '{_password}' WHERE username = '{username}';")
                database.commit()
                database.close()
            elif choice == 2:

                # TODO waarom loopen?
                loop = True
                count = 0
                user = Helper().checkLoggedIn()
                database = Database("analyse.db")
                while loop:
                    data = database.get(columns='*', table=f'{"Advisors"}')

                    database.commit()
                    try:
                        for row in data:
                            print("ID          |", row[0])
                            print("Firstname   |", Helper().Decrypt(row[1]))
                            print("Lastname    |", Helper().Decrypt(row[2]))
                            print("Username    |", Helper().Decrypt(row[3])), "\n"
                            loop = False

                    except:
                        print("Person not found, try again. excpet")
                try:

                    username = input("What is the username of the advisor: ")

                    username = Helper().Encrypt(username)
                    _password = input(
                        "What will be ur password? Min length of 8, no longer than 30 characters, MUST have at least one lowercase letter, one uppercase letter, one digit and one special character :")
                    password = Helper().passwordchecker  # TODO check this function
                    kind = "Advisors"
                    _password = Helper().Encrypt(_password)
                    database.query(f"UPDATE {kind} SET password = '{_password}' WHERE username = '{username}';")
                    database.commit()
                    database.close()
                except:
                    print("Person not found. Try again.")
            else:
                print("Wrong input. try again")

    # def checkUsers(self, kind):
    #     loop = True
    #     database = Database("analyse.db")
    #     while loop:
    #         choice = userinterface.choices(["Check Advisors", "Check System Administrators", "Check Super Administrator"],
    #                             "Who do you want to view?: ")
    #         _type = None
    #         if choice == 1:
    #             loop = False
    #             print("Hello")
    #             _type = 'Advisors'
    #             # Display data
    #             print('\nAdvisors: \n')
    #             data = database.get(columns='*', table=f'{_type}')
    #             for row in data:
    #                 print("ID          |", row[0])
    #                 print("Firstname   |", Helper().Decrypt(row[1]))
    #                 print("Lastname    |", Helper().Decrypt(row[2]))
    #                 print("Username    |", Helper().Decrypt(row[3]))
    #                 print("Role        | Advisor\n")
    #
    #
    #         elif choice == 2:
    #             _type = 'SystemAdmins'
    #             print('\SystemAdmins: \n')
    #             data = database.get(columns='*', table=f'{_type}')
    #             for row in data:
    #                 print(row)
    #                 print("ID          |", row[0])
    #                 print("Firstname   |", Helper().Decrypt(row[1]))
    #                 print("Lastname    |", Helper().Decrypt(row[2]))
    #                 print("Username    |", Helper().Decrypt(row[3]))
    #                 print("Role        | SystemAdmin\n")
    #             loop = False
    #         elif choice == 3:
    #             _type = 'SuperAdmin'
    #             print('SuperAdmin: \n')
    #             data = database.get(columns='*', table=f'{_type}')
    #             for row in data:
    #                 print("ID          |", row[0])
    #                 print("Firstname   |", Helper().Decrypt(row[1]))
    #                 print("Lastname    |", Helper().Decrypt(row[2]))
    #                 print("Username    |", Helper().Decrypt(row[3]))
    #                 print("Role        | SuperAdmin\n")
    #             loop = False
    #         else:
    #             print("Incorrect input, try again.")
    #
    #     database.close()

    def checkUsers(self, kind):
        # kind kunnen we hier gebruiken?
        from src.cdms.userinterfaceClass import userinterface
        loop = True
        database = Database("analyse.db")
        while loop:
            choice = userinterface().choices(
                choices=["Check Advisors", "Check System Administrators", "Check Super Administrator"],
                question="Who do you want to view?: ")  # TODO check regular memebers
            _type = None
            if choice == 1:
                _type = 'Advisors'
            elif choice == 2:
                _type = 'SystemAdmins'
            elif choice == 3:
                _type = 'SuperAdmin'
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
                print("Role        | SystemAdmin\n")
            loop = False

        database.close()
