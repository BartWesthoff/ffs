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
            firstname = Validator().is_valid_name(input("What is your firstname?: "))
            firstname = Helper().encrypt(firstname)

            lastname = Validator().is_valid_name(input("What is your lastname?: "))
            lastname = Helper().encrypt(lastname)

            username = Helper().username_checker(input("What is your username?: "))
            username = Helper().encrypt(username)

            password = Validator().is_valid_password(input("What is your password?: "))
            password = Helper().encrypt(password)

            registration_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            uuid = Helper.generate_uuid()
            database.create_employee(kind=kind, firstname=firstname, lastname=lastname, username=username,
                                     password=password, id=uuid, registration_date=registration_date)
            database.add_log(
                    description=f"Created a {kind}.",
                    suspicious="no")
        elif kind.lower() == "member":
            Member().create_member()
        database.commit()
        database.close()

    def search_member(self, kind):
        database = Database("analyse.db")
        data = database.get(columns='*', table=kind)
        if not data:
            print(f"No {kind}'s found.")
        else:
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

    def search_employee_username(self, kind, username):
        database = Database("analyse.db")
        data = database.search_employee_by_username(kind=kind, username=Helper.encrypt(username))
        people = []

        for row in data:
            user = User.to_user_decrypt(row)
            if user.search_user(search_term=username.lower()):
                people.append(user)

        database.close()
        return people[0]

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
            return people

        for person in people:
            print(person)
            print("list of people found")

        database.close()
        return people

    def delete_person(self, kind):
        kind = kind.lower()
        database = Database("analyse.db")
        people = self.search_member(kind=kind)

        print(people[0].id)
        for person in people:
            print(Helper.encrypt(person.username))
            data = database.search_person(kind=kind, firstname=Helper.encrypt(person.firstname),
                                          lastname=Helper.encrypt(person.lastname))
            print(data)
            if data is not None:
                database.delete_person(table=kind, firstname=Helper.encrypt(person.firstname),
                                       lastname=Helper.encrypt(person.lastname))
                database.commit()
                print(f"{person.firstname} {person.lastname} Deleted")

    def delete_employee(self, kind):
        kind = kind.lower()
        database = Database("analyse.db")
        people = self.search_employee(kind=kind)

        print(people[0].id)
        for person in people:
            print(Helper.encrypt(person.username))
            data = database.search_employee(kind=kind, firstname=Helper.encrypt(person.firstname),
                                            lastname=Helper.encrypt(person.lastname),
                                            username=Helper.encrypt(person.username))
            print(data)
            if data is not None:
                database.delete_employee(table=kind, firstname=Helper.encrypt(person.firstname),
                                         lastname=Helper.encrypt(person.lastname),
                                         username=Helper.encrypt(person.username))
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
        attr = Advisor.get_attributes()  # ["username", "firstname", "lastname"]
        for row in data:
            print(row)
            user = User.to_user_decrypt(row)

            if user.search_user(search_key.lower()):
                people.append(user)
        if len(people) == 0:
            print("No people found, try again.")
            self.modify_member(kind=kind)

        for person in people:
            print(person)
            print("list of people found")

        choices = []
        for att in attr:
            choices.append(f"Modify {att}")
        choice = UserInterface().choices(choices)

        new_data = input(f"What will be the new {attr[choice - 1]}: ")

        person_to_modify = people[0]
        old_firstname = Helper().encrypt(person_to_modify.firstname)
        old_lastname = Helper.encrypt(person_to_modify.lastname)
        old_username = Helper.encrypt(person_to_modify.username)
        for _ in attr:
            # TODO mooier neerzetten
            if choice != 2:
                new_data = Validator().is_valid_name(new_data)
            else:
                new_data = Validator().is_valid_password(new_data)
        person_to_modify = User.to_user_encrypt(person_to_modify)
        new_data = Helper().encrypt(new_data)
        if choice == 1:
            person_to_modify.username = new_data
        elif choice == 2:
            person_to_modify.password = new_data
        elif choice == 3:
            person_to_modify.firstname = new_data
        elif choice == 4:
            person_to_modify.lastname = new_data

        database.update_user(kind=kind, firstname=person_to_modify.firstname, lastname=person_to_modify.lastname,
                             username=person_to_modify.username, password=person_to_modify.password,
                             id=person_to_modify.id, old_firstname=old_firstname,
                             old_lastname=old_lastname, registration_date=person_to_modify.registration_date,
                             old_username=old_username)
        database.commit()
        database.close()

    def modify_member(self, kind):
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

        attr = Member.get_attributes()
        for row in data:
            member = Member.to_member_decrypt(row)
            if member.search_member(search_term=search_key.lower()):
                people.append(member)

        for person in people:
            print(person)
            print("list of people found")

        if len(people) == 0:
            print("No people found, try again.")
            self.modify_member(kind=kind)

        person_to_modify = people[0]
        choices = []
        for att in attr:
            choices.append(f"Modify {att}")
        choice = UserInterface().choices(choices)

        if choice == 7:
            list_of_cities = ["Rotterdam", "Amsterdam", "Alkmaar", "Maastricht", "Utrecht", "Almere", "Lelystad",
                              "Maassluis",
                              "Vlaardingen", "Schiedam"]
            city_index = UserInterface().choices(choices=list_of_cities, question="Please select a city: ")
            new_data = list_of_cities[city_index - 1]
        else:
            new_data = input(f"What will be the new {attr[choice - 1]}: ")
        old_firstname = Helper().encrypt(person_to_modify.firstname)
        old_lastname = Helper.encrypt(person_to_modify.lastname)
        for _ in attr:
            # TODO mooier neerzetten
            if choice == 1:
                new_data = Validator().is_valid_name(new_data)
                person_to_modify.firstname = new_data
            if choice == 2:
                new_data = Validator().is_valid_name(new_data)
                person_to_modify.lastname = new_data
            elif choice == 3:
                new_data = Validator().is_valid_email(new_data)
                person_to_modify.email = new_data
            elif choice == 4:
                new_data = Validator().is_valid_name(new_data)
                person_to_modify.street = new_data
            elif choice == 5:
                new_data = Validator().is_valid_number(new_data)
                person_to_modify.house_number = new_data
            elif choice == 6:
                new_data = Validator().is_valid_zipcode(new_data)
                person_to_modify.zipcode = new_data
            elif choice == 7:
                new_data = Validator().is_valid_name(new_data)
                person_to_modify.city = new_data
            elif choice == 8:
                new_data = Validator().is_valid_phone_number(new_data)
                person_to_modify.phone_number = new_data
        person_to_modify = Member.to_member_encrypt(person_to_modify)
        database.update_member(member=person_to_modify, old_firstname=old_firstname, old_lastname=old_lastname)
        database.close()

    def change_password(self, kind, access):
        kind = kind.lower()
        database = Database("analyse.db")
        # TODO even checken of kind permissie heeft voor het veranderen van wachtworden
        from src.cdms.userinterfaceClass import UserInterface
        from src.cdms.userinterfaceClass import Role

        actions = [("Reset an advisors password.", Role.SYSTEM_ADMINISTATOR),
                   ("Reset an systemadmin password.", Role.SUPER_ADMINISTATOR)]

        if access != Role.SUPER_ADMINISTATOR:
            actions.append(("Reset own password.", Role.ADVISOR))

        allowed_actions = [action for action in actions if action[1] <= access]
        choice = UserInterface().choices([action[0] for action in allowed_actions])
        action_to_perform = allowed_actions[choice - 1][0]

        print(action_to_perform)

        if action_to_perform == "Reset an advisors password.":
            kind = "advisor"
        if action_to_perform == "Reset an systemadmin password.":
            kind = "systemadmin"

        if action_to_perform == "Reset own password.":
            user = self.search_employee_username(kind=kind, username=Helper().check_logged_in())
        else:
            user = self.search_employee(kind=kind)

        if user is None or len(user) == 0:
            return None
        print(user)

        person_to_modify = user[0]
        username_target = person_to_modify.username
        new_password = input(
            "What will be the password? Min length of 8, no longer than 30 characters, MUST have at least one "
            "lowercase letter, one uppercase letter, one digit and one special character : ")
        password = Validator().is_valid_password(password=new_password)
        password = Helper().encrypt(password)

        print(f"{password=}")
        print(f"{kind=}")
        user = User.to_user_encrypt(person_to_modify)
        database.update_password(kind=kind, username=Helper.encrypt(person_to_modify.username), password=password, user=user)

        username_user = Helper().decrypt(person_to_modify.username)
        database.add_log(
            description=f"{username_user} changed password for {person_to_modify.username} to {Helper().decrypt(password)}",
            suspicious="no")

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
                    if not data:
                        print("No users found.")
                    else:
                        for row in data:
                            print(f"Role        | {user_type}\n")
                            print("ID          |", row[0])
                            print("Firstname   |", Helper().decrypt(row[1]))
                            print("Lastname    |", Helper().decrypt(row[2]))
                            print("Username    |", Helper().decrypt(row[3]))

            else:
                data = database.get(columns='*', table=_type)
                if not data:
                    print(f"No {_type}'s found.\n")
                else:
                    for row in data:
                        # print(row)
                        print(f"Role        | {_type}\n")
                        print("ID          |", row[0])
                        print("Firstname   |", Helper().decrypt(row[1]))
                        print("Lastname    |", Helper().decrypt(row[2]))
                        print("Username    |", Helper().decrypt(row[3]))


            loop = False

        database.close()
