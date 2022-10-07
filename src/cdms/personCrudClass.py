from src.cdms.InputValidationClass import Validator
from src.cdms.databaseclass import Database
from src.cdms.helperClass import Helper
from src.cdms.memberClass import Member



# TODO deze hele class testen

class PersonCRUD:

    @staticmethod
    def add_person(kind):
        kind = kind.lower()
        database = Database("analyse.db")
        if kind.lower() in ["advisor", "systemadmin"]:
            firstname = input("firstname?: ")
            firstname = Helper().encrypt(firstname)
            lastname = input("lastname?: ")
            lastname = Helper().encrypt(lastname)
            username = input("username?:")
            username = Helper().username_checker(username)
            username = Helper().encrypt(username)
            password = input("password?: ")
            password = Helper().password_checker(password)
            password = Helper().encrypt(password)

            database.create_employee(kind, firstname, lastname, username, password)

        elif kind.lower() == "member":
            Member().create_member()
        database.commit()
        database.close()

    @staticmethod
    def search_person(kind):
        kind = kind.lower()
        loop = True
        count = 0
        user = Helper().check_logged_in()
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            print("ID          |", row[0])
            print("Firstname   |", Helper().decrypt(row[1]))
            print("Lastname    |", Helper().decrypt(row[2]) + "\n")

        while loop:
            
            id = input("ID?: ")
            id = Validator().is_valid_number(id)
            data = database.search_person_by_id(kind=kind, id=id)
            database.commit()
            if data is not None:

                member = Member().to_member(data)
                # TODO hier kunnen we denk de __str__ in de member class gebruiken
                print("UUID          |", member.uuid)
                print("Firstname     |", Helper.decrypt(member.firstname))
                print("Lastname      |", Helper.decrypt(member.lastname))
                print("Street        |", Helper.decrypt(member.street))
                print("Housenumber   |", Helper.decrypt(member.house_number))
                print("Zipcode       |", Helper.decrypt(member.zipcode))
                print("City          |", Helper.decrypt(member.city))
                print("mail          |", Helper.decrypt(member.mail))
                print("Phone         |", Helper.decrypt(member.mobile_number))
                print("creation date |", member.registration_date)

                loop = False
            elif data is None:
                print("Member not found, try again.")

        database.close()

    @staticmethod
    def delete_person(kind):
        kind = kind.lower()
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            print("ID          |", row[0])
            print("Firstname   |", Helper().decrypt(row[1]))
            print("Lastname    |", Helper().decrypt(row[2]))
            print(f"Role        | {kind}\n")

        firstname = input("firstname?: ")
        firstname = Validator().is_valid_name(firstname)

        lastname = input("lastname?: ")
        lastname = Validator().is_valid_name(lastname)

        firstname = Helper().encrypt(firstname)
        lastname = Helper().encrypt(lastname)

        data = database.search_person(kind=kind, firstname=firstname, lastname=lastname)
        if data is not None:
            database.delete_person(table=kind, firstname=firstname, lastname=lastname)
            database.commit()
            print("Deleted")
        else:
            print("Person not found, Try again.\n")

    def modify_person(self, kind):
        #TODO circulaire import
        from src.cdms.userinterfaceClass import UserInterface
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            print(row)
            print("ID          |", row[0])
            print("Firstname   |", Helper().decrypt(row[1]))
            print("Lastname    |", Helper().decrypt(row[2]))
            print(f"Role        | {kind}\n")

        _firstname = input(f"What is the firstname of the {kind}?: ")
        _firstname = Validator().is_valid_name(_firstname)

        _lastname = input(f"What is the lastname of the {kind}?: ")
        _lastname = Validator().is_valid_name(_lastname)

        _firstname = Helper().encrypt(_firstname)
        _lastname = Helper().encrypt(_lastname)
        data = database.search_person(kind=kind, firstname=_firstname, lastname=_lastname)
        if data is None:
            print("Member not found, try again.")
            self.modify_person(kind)
        attr = ["firstname", "lastname", "streetname", "housenumber", "zipcode", "city", "emailaddress", "mobilephone"]
        choices = []
        for att in attr:
            choices.append(f"Modify {att}")
        choice = UserInterface().choices(choices)

        new_data = input(f"What will be the new {attr[choice - 1]}: ")
        for _ in attr:
            # TODO mooier neerzetten
            if choice == 1 or choice == 2:
                new_data = Validator().is_valid_name(new_data)
            elif choice == 3:
                new_data = Validator().is_valid_streetname(new_data)
            elif choice == 4:
                new_data = Validator().is_valid_number(new_data)
            elif choice == 5:
                new_data = Validator().is_valid_zipcode(new_data)
            elif choice == 6:
                new_data = Validator().is_valid_zipcode(new_data)
            elif choice == 7:
                new_data = Validator().is_valid_email(new_data)
            elif choice == 8:
                new_data = Validator().is_valid_email(new_data)

        new_data = Helper().encrypt(new_data)
        database.query(
            f"UPDATE {kind} SET {attr[choice - 1]} = ? WHERE firstname = ? AND lastname = ?;",
            (new_data, _firstname, _lastname))
        database.commit()
        database.close()

    @staticmethod
    def change_password(kind):
        kind = kind.lower()
        database = Database("analyse.db")
        ## TODO even checken of kind permissie heeft voor het veranderen van wachtworden
        from src.cdms.userinterfaceClass import UserInterface
        from src.cdms.userinterfaceClass import Role
        role = Role.EMPTY
        if kind == "advisor":
            role = Role.ADVISOR
        elif kind == "superadmin":
            role = Role.SUPER_ADMINISTATOR
        elif kind == "systemadmin":
            role = Role.SYSTEM_ADMINISTATOR
        actions = [("Reset own password.", Role.ADVISOR ), ("Reset an advisors password.", Role.SYSTEM_ADMINISTATOR),
                   ("Reset an systemadmin password.", Role.SUPER_ADMINISTATOR)]
        allowed_actions = [action for action in actions if action[1] <= role]
        choice = UserInterface().choices( [action[0] for action in allowed_actions])
        action_to_perform = allowed_actions[choice - 1][0]
        username_target = None
        print(action_to_perform)

        if action_to_perform == "Reset an advisors password.":
            kind = "advisor"
        if action_to_perform == "Reset an systemadmin password.":
            kind = "systemadmin"

        if action_to_perform == "Reset an advisors password." or action_to_perform == "Reset an systemadmin password, ":

            username_target = Validator().is_valid_name(username_target)
            data = database.get_all_of_kind(kind=kind)
            if data is not None:
                for enity in data:
                    print("id                | ", enity[0])
                    print("firstname         | ", Helper.decrypt(enity[1]))
                    print("lastname          | ", Helper.decrypt(enity[2]))
                    print("username          | ", Helper.decrypt(enity[3]))
                    print("password          | ", Helper.decrypt(enity[4]))

                username_target = input(f"What is the username of the {kind}: ")
                username_target = Helper().encrypt(username_target)

        username_user = Helper().check_logged_in()



        _password = input(
            "What will be the password? Min length of 8, no longer than 30 characters, MUST have at least one "
            "lowercase letter, one uppercase letter, one digit and one special character : ")
        password = Helper().password_checker(password=_password)
        password = Helper().encrypt(password)
        print(f"{password=}")
        username_to_change = username_user if action_to_perform == "Reset own password." else username_target
        print(f"{username_to_change=}")
        print(f"{kind=}")
        database.update_password(kind=kind, username=username_to_change, password=password)
        username_user = Helper().decrypt(username_user)
        database.add_log(
            description=f"{username_user} changed password for {username_to_change} to {Helper().decrypt(password)}",
            suspicious="yes")

        database.commit()
        database.close()

    @staticmethod
    def check_users():
        from src.cdms.userinterfaceClass import UserInterface
        loop = True
        database = Database("analyse.db")
        while loop:
            choice = UserInterface().choices(
                ["Check Advisors", "Check System Administrators",
                 "Check Super Administrator"])
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
                print("Firstname   |", Helper().decrypt(row[1]))
                print("Lastname    |", Helper().decrypt(row[2]))
                print("Username    |", Helper().decrypt(row[3]))
                print(f"Role        | {_type}\n")
            loop = False

        database.close()
