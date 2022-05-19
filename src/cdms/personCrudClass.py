from src.cdms.clientClass import Client
from src.cdms.databaseclass import Database
from src.cdms.helperClass import Helper


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

        elif kind.lower() == "client":
            # client = Client().dummyClient()  # todo change to real client
            client = Client().createClient()
            database.createClient(client)
        database.commit()
        database.close()

    @staticmethod
    def searchPerson(kind):
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
            # data = database.get(columns='*', table=f'{kind}',
            #                     where=f"`firstname`='{firstname}' AND `lastname`='{lastname}'")
            data = database.searchPerson(kind=kind, firstname=firstname, lastname=lastname)
            database.commit()
            if data is not None:

                client = Client().toClient(data)

                print("ID            |", client.id)
                print("Firstname     |", Helper.Decrypt(client.firstname))
                print("Lastname      |", Helper.Decrypt(client.lastname))
                print("Street        |", Helper.Decrypt(client.street))
                print("Housenumber   |", client.housenumber)
                print("Zipcode       |", Helper.Decrypt(client.zipcode))
                print("City          |", Helper.Decrypt(client.city))
                print("mail          |", Helper.Decrypt(client.mail))
                print("Phone         |", client.mobile_number)
                print("creation date |", client.registration_date)

                loop = False
            elif data is None:
                print("Client not found, try again.")

        database.close()

    @staticmethod
    def deletePerson(kind):
        database = Database("analyse.db")
        firstname = input("firstname?: ")

        lastname = input("lastname?: ")
        firstname = Helper().Encrypt(firstname)
        lastname = Helper().Encrypt(lastname)
        print(firstname)
        print(lastname)

        data = database.get(columns='*', table=f'{kind}',
                            where=f"`firstname`='{firstname}' AND `lastname`='{lastname}'")
        if data is not None:
            print(data)
            # database.query(f"DELETE FROM "systemadmin" WHERE 'firstname'='{firstname}' AND 'lastname'='{lastname}'")
            database.query(f"DELETE FROM '{kind}' WHERE firstname='{firstname}' AND lastname='{lastname}'")
            database.commit()

            print("Deleted")

    def modifyPerson(self, kind):
        from src.cdms.userinterfaceClass import userinterface
        database = Database("analyse.db")
        _firstname = input(f"What is the firstname of the {kind}?: ")
        _lastname = input(f"What is the lastname of the {kind}?: ")
        _firstname = Helper().Encrypt(_firstname)
        _lastname = Helper().Encrypt(_lastname)
        data = database.searchPerson(kind=kind, firstname=_firstname, lastname=_lastname)
        if data is None:
            print("Client not found, try again.")
            self.modifyPerson(kind)
        attr = ["firstname", "lastname"]
        choices = []
        for att in attr:
            choices.append(f"Modify {att}")
        choice = userinterface().choices(choices)

        new_data = input(f"What will be the new {attr[choice - 1]}")
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
                print("Role        | SystemAdmin\n")
            loop = False

        database.close()
