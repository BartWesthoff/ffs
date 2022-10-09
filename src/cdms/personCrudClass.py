import datetime

from src.cdms.InputValidationClass import Validator
from src.cdms.UserClass import User
from src.cdms.advisorClass import Advisor
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
            firstname = Validator().is_valid_name(input("What is your Firstname?: "))
            firstname = Helper().encrypt(firstname)

            lastname = Validator().is_valid_name(input("What is your Lastname?: "))
            lastname = Helper().encrypt(lastname)

            username = Helper().username_checker(input("username?: "))
            username = Helper().encrypt(username)

            password = Validator().is_valid_password(input("password?: "))
            password = Helper().encrypt(password)

            registration_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            id = Helper.generate_uuid()
            database.create_employee(kind=kind, firstname=firstname, lastname=lastname, username=username,
                                     password=password, id=id, registration_date=registration_date)

        elif kind.lower() == "member":
            Member().create_member()
        database.commit()
        database.close()

    def search_member(self, kind):
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            # print(row)
            print("ID          |", row[0])
            print("Firstname   |", Helper().decrypt(row[1]))
            print("Lastname    |", Helper().decrypt(row[2]))
            print(f"Role        | {kind}\n")
        people = []
        print("Please fill in ID, firstname, lastname, address, e-mailadress or phonenumber of the person you want to "
              "modify.")
        search_key = input("Who do you want to search?: ")
        for row in data:
            member = Member.to_member_decrypt(row)
            if member.search_member(search_term=search_key.lower()):
                people.append(member)

        if len(people) == 0:
            print("No people found, try again.")
            self.search_member(kind=kind)

        for person in people:
            print(person)
            print("list of people found")

        database.close()
        return people

    def search_employee(self, kind):
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            # print(row)
            print("ID          |", row[0])
            print("Firstname   |", Helper().decrypt(row[1]))
            print("Lastname    |", Helper().decrypt(row[2]))
            print(f"Role        | {kind}\n")
        people = []
        print("Please fill in ID, firstname, lastname, address, e-mailadress or phonenumber of the person you want to "
              "modify.")
        search_key = input("Who do you want to search?: ")
        for row in data:
            user = User.to_user_decrypt(row)
            if user.search_user(search_term=search_key.lower()):
                people.append(user)

        if len(people) == 0:
            print("No people found, try again.")
            self.search_employee(kind=kind)

        for person in people:
            print(person)
            print("list of people found")

        database.close()
        return people

    def delete_person(self, kind):
        from src.cdms.userinterfaceClass import UserInterface
        kind = kind.lower()
        database = Database("analyse.db")
        # data = database.get(columns='*', table=kind)
        # for row in data:
        #     print("ID          |", row[0])
        #     print("Firstname   |", Helper().decrypt(row[1]))
        #     print("Lastname    |", Helper().decrypt(row[2]))
        #     print(f"Role        | {kind}\n")
        # if kind == "member":
        #     members = []
        #     for row in data:
        #         member = Member.to_member_decrypt(row)
        #         members.append(member)
        people = []
        if kind == "member":
            people = self.search_member(kind=kind)
        elif kind == "advisor" or kind == "systemadmin":
            people = self.search_employee(kind=kind)
        else:
            print("No people found, try again.")
            UserInterface().main_screen()
        print(people[0].id)
        for person in people:
            print(Helper.encrypt(person.username))
            data = database.search_person(kind=kind, firstname=Helper.encrypt(person.firstname), lastname=Helper.encrypt(person.lastname))
            print(data)
            if data is not None:
                database.delete_person(table=kind, firstname=Helper.encrypt(person.firstname), lastname=Helper.encrypt(person.lastname), username=Helper.encrypt(person.username))
                database.commit()
                print(f"{person.firstname} {person.lastname} Deleted")


    def modify_user(self, kind):
        # TODO circulaire import
        from src.cdms.userinterfaceClass import UserInterface
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            # print(row)
            print("ID          |", row[0])
            print("Firstname   |", Helper().decrypt(row[1]))
            print("Lastname    |", Helper().decrypt(row[2]))
            print(f"Role        | {kind}\n")
        people = []
        print("Please fill in ID, firstname, lastname, address, e-mailadress or phonenumber of the person you want to "
              "modify.")
        search_key = input("Who do you want to modify?: ")
        attr = Advisor.get_attributes()  # ["username", "password", "firstname", "lastname"]
        for row in data:
            print(row)
            user = User.to_user_decrypt(row)

            if user.search_user(search_key.lower()):
                people.append(user)
        if len(people) == 0:
            print("No people found, try again.")
            self.modify_person(kind=kind)

        for person in people:
            print(person)
            print("list of people found")

        choices = []
        for att in attr:
            choices.append(f"Modify {att}")
        choice = UserInterface().choices(choices)

        new_data = input(f"What will be the new {attr[choice - 1]}: ")
        for _ in attr:
            # TODO mooier neerzetten
            if choice != 2:
                new_data = Validator().is_valid_name(new_data)
            else:
                new_data = Validator().is_valid_password(new_data)

        new_data = Helper().encrypt(new_data)

        print(people[0].id)
        database.query(
            f"UPDATE {kind} SET {attr[choice - 1]} = ? WHERE id = ?;",
            (new_data, Helper.encrypt(people[0].id)))
        database.commit()
        database.close()

    def modify_person(self, kind):
        # TODO circulaire import
        from src.cdms.userinterfaceClass import UserInterface
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        for row in data:
            # print(row)
            print("ID          |", row[0])
            print("Firstname   |", Helper().decrypt(row[1]))
            print("Lastname    |", Helper().decrypt(row[2]))
            print(f"Role        | {kind}\n")
        people = []
        print("Please fill in ID, firstname, lastname, address, e-mailadress or phonenumber of the person you want to "
              "modify.")
        search_key = input("Who do you want to modify?: ")
        attr = []
        if kind == "member":
            attr = Member.get_attributes()
            for row in data:
                member = Member.to_member_decrypt(row)
                if member.search_member(search_term=search_key.lower()):
                    people.append(member)

        if kind == "advisor":
            attr = Advisor.get_attributes()
            for row in data:
                print(row)
                advisor = Advisor.to_advisor_decrypt(row)

                if advisor.search_advisor(search_key.lower()):
                    people.append(advisor)

        for person in people:
            print(person)
            print("list of people found")

        # _firstname = input(f"What is the firstname of the {kind}?: ")
        # _firstname = Validator().is_valid_name(_firstname)
        #
        # _lastname = input(f"What is the lastname of the {kind}?: ")
        # _lastname = Validator().is_valid_name(_lastname)
        #
        # _firstname = Helper().encrypt(_firstname)
        # _lastname = Helper().encrypt(_lastname)
        if len(people) == 0:
            print("No people found, try again.")
            self.modify_person(kind=kind)

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
                new_data = Validator().is_valid_name(new_data)
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

        print(people[0].id)
        database.query(
            f"UPDATE {kind} SET {attr[choice - 1]} = ? WHERE id = ?;",
            (new_data, Helper.encrypt(people[0].id)))
        database.commit()
        database.close()

    @staticmethod
    def change_password(kind):
        kind = kind.lower()
        database = Database("analyse.db")
        # TODO even checken of kind permissie heeft voor het veranderen van wachtworden
        from src.cdms.userinterfaceClass import UserInterface
        from src.cdms.userinterfaceClass import Role
        # role = Role.EMPTY
        role = ["advisor", "superadmin", "systemadmin"].index(kind) + 1
        # if kind == "advisor":
        #     role = Role.ADVISOR
        # elif kind == "superadmin":
        #     role = Role.SUPER_ADMINISTATOR
        # elif kind == "systemadmin":
        #     role = Role.SYSTEM_ADMINISTATOR
        actions = [("Reset own password.", Role.ADVISOR), ("Reset an advisors password.", Role.SYSTEM_ADMINISTATOR),
                   ("Reset an systemadmin password.", Role.SUPER_ADMINISTATOR)]
        allowed_actions = [action for action in actions if action[1] <= role]
        choice = UserInterface().choices([action[0] for action in allowed_actions])
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
        password = Validator().is_valid_password(password=_password)
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
        data = None
        while data is None:
            choice = UserInterface().choices(
                ["Check Advisors", "Check System Administrators", "Check Super Administrator", "All users"])
            _type = "all"
            if choice == 1:
                _type = "advisor"
            elif choice == 2:
                _type = "systemadmin"
            elif choice == 3:
                _type = "superadmin"
            elif choice == 4:
                _type = "all"
            else:
                print("Incorrect input, try again.")

            print("")  # voor wat ruimte
            if _type == "all":
                for user_type in ["advisor", "systemadmin", "superadmin"]:
                    data = database.get(columns='*', table=user_type)
                    for row in data:
                        print(row)
                        user = User.to_user_decrypt(row)
                        print(f"Role: {user_type.capitalize()}")
                        print(user)

            elif _type in ["advisor", "systemadmin", "superadmin"]:
                data = database.get(columns='*', table=_type)
                for row in data:
                    print(row)
                    user = User.to_user_decrypt(row)
                    print(f"Role: {_type.capitalize()}")
                    print(user)
            else:
                print("Wrong type of user, try again.")
                PersonCRUD.check_users()

        database.close()
