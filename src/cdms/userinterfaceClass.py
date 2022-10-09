from src.cdms.databaseclass import Database
from src.cdms.exceptions import Exceptions
from src.cdms.helperClass import Helper
from src.cdms.menus import menu

from src.cdms.personCrudClass import PersonCRUD


class Role:
    EMPTY = 0
    ADVISOR = 1
    SYSTEM_ADMINISTATOR = 2
    SUPER_ADMINISTATOR = 3


class UserInterface:

    def main_screen(self):
        database = Database("analyse.db")
        database.check_migrations()
        database.close()

        choice: int = self.choices(["Login", "Exit application"])
        if choice == 1:
            self.login_screen()
        if choice == 2:
            Helper().stop_app()
        else:
            Exceptions.bad_error()
            self.main_screen()
            

    def login_screen(self):
        loop = True
        login_username = ""
        usernames = []
        passwords = []
        tries = 0
        _type = ""
        type = Role.EMPTY
        choice = self.choices(["advisor", "System administrators", "Super administrator"])

        if choice == 1:
            _type = "advisor"
            type = Role.ADVISOR
        elif choice == 2:
            _type = "systemadmin"
            type = Role.SYSTEM_ADMINISTATOR
        elif choice == 3:
            _type = "superadmin"
            type = Role.SUPER_ADMINISTATOR
        else:
            Exceptions.bad_error()
            self.login_screen()

        while loop:
            if tries == 3:
                print("3 wrong tries, incident logged.")
                database = Database("analyse.db")
                Helper().log_username("")
                database.add_log(
                    description=f"3 wrong tries combinations {[(user) for user in zip(usernames)]}.",
                    suspicious="yes")
                Helper().stop_app()

            login_username = input("What is your username?: ")
            Helper().log_username(login_username)

            login_password = input("What is your password?: ")

            passwords.append(login_password)
            usernames.append(login_username)

            if login_password == "a" and login_username == "a":
                database = Database("analyse.db")
                database.add_log(
                    description=f"logged in",
                    suspicious="no")
                break

            login_username = Helper().encrypt(login_username)
            login_password = Helper().encrypt(login_password)
            database = Database("analyse.db")

            data = database.login(kind=_type, username=login_username, password=login_password)
            # data = database.login(kind=str(type), username=login_username, password=login_password)

            if not data:
                Helper().log_username("")
                database.add_log(
                    description=f"Unsuccesful login for {[(user) for user in zip(usernames)]}. ",
                    suspicious="no")
                print("Wrong username or password, try again.\n")
                tries += 1
            else:
                database.add_log(
                    description=f"logged in",
                    suspicious="no")
                break
        
        
        menu(type)

    def choices(self, choices, question="Which option do you want to choose? Pick a number: "):
        for idx, choice in enumerate(choices):
            print(f"{idx+1}. {choice}")
        c = input(question)

        if c.isnumeric() and len(choices) >= int(c) > 0:
            return int(c)
        else:
            print("Wrong number")
            self.choices(choices, question)