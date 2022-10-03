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
            Helper().stop_app()

    def login_screen(self):
        loop = True
        login_username = ""
        usernames = []
        passwords = []
        tries = 0
        _type = ""
        # type = Role.EMPTY
        choice = self.choices(["advisor", "System administrators", "Super administrator"])

        if choice == 1:
            # _type = "advisor"
            type = Role.ADVISOR
        elif choice == 2:
            # _type = "systemadmin"
            type = Role.SYSTEM_ADMINISTATOR
        elif choice == 3:
            # _type = "superadmin"
            type = Role.SUPER_ADMINISTATOR
        else:
            Exceptions.bad_error()
            Helper().stop_app()
            self.login_screen()

        while loop:
            if tries == 3:
                print("3 wrong tries, incident logged.")
                database = Database("analyse.db")
                database.add_log(
                    description=f"3 wrong tries combinations {[(user, pw) for user, pw in zip(usernames, passwords)]}.",
                    suspicious="yes")
                Helper().stop_app()

            login_username = input("What is your username?: ")
            login_password = input("What is your password?: ")

            passwords.append(login_password)
            usernames.append(login_username)

            if login_password == "Admin321!" and login_username == "superadmin":
                break

            login_username = Helper().encrypt(login_username)
            login_password = Helper().encrypt(login_password)
            database = Database("analyse.db")

            data = database.login(kind=_type, username=login_username, password=login_password)
            # data = database.login(kind=str(type), username=login_username, password=login_password)

            if not data:
                print("Wrong username or password, try again.\n")
                tries += 1
            else:
                break

        Helper().log_username(login_username)

        if _type == "advisor":
            self.advisor_menu()
        if _type == "systemadmin":
            self.system_administator_menu()
        if _type == "superadmin":
            self.super_admin_menu()

        # TODO  onderstaand gebruiken en dan die if statements boven wegdoen
        menu(type)

    def choices(self, choices, question="Which option do you want to choose?: "):
        for idx, choice in enumerate(choices):
            print(f"{idx+1}. {choice}")
        c = input(question)

        if c.isnumeric() and len(choices) >= int(c) > 0:
            return int(c)
        else:
            print("Wrong number")
            self.choices(choices, question)


    # TODO NIELS: menu kan vervangen worden door menus(Role.SUPER_ADMINISTATOR)
    def super_admin_menu(self):
        callToAction = {
            "List of users": PersonCRUD().check_users,
            'Check member': PersonCRUD().search_person,
            'add member': PersonCRUD().add_person,
            'Modify member': PersonCRUD().modify_person,
            'Delete member': PersonCRUD().delete_person,
            'add a new advisor': PersonCRUD().add_person,
            'Modify advisor': PersonCRUD().modify_person,
            'Delete advisor': PersonCRUD().delete_person,
            "chang password": PersonCRUD().change_password,
            "add a new system administrator": PersonCRUD().add_person,
            'Modify system administrator': PersonCRUD().modify_person,
            'Delete system administrator': PersonCRUD().delete_person,
            "make a backup": Helper().make_backup,
            "restore a backup": Helper().restore_backup,
            "see log(s)": Helper().see_logs,
            "Logout": UserInterface().main_screen

        }
        options = list(callToAction.keys())
        choice = self.choices(options)

        if choice == 1:
            callToAction[options[choice - 1]]()
            self.super_admin_menu()
        if choice in [2, 3, 4, 5]:
            callToAction[options[choice - 1]]("member")
            self.super_admin_menu()
        elif choice in [6, 7, 8]:
            callToAction[options[choice - 1]]("advisor")
            self.super_admin_menu()

        elif choice in [9]:
            callToAction[options[choice - 1]]("superadmin")
            self.super_admin_menu()
        elif choice == 10:
            callToAction[options[choice - 1]]("systemadmin")
            self.super_admin_menu()
        elif choice == 11:
            callToAction[options[choice - 1]]("systemadmin")
            self.super_admin_menu()
        elif choice == 12:
            callToAction[options[choice - 1]]("systemadmin")
            self.super_admin_menu()
        elif choice == 13:
            callToAction[options[choice - 1]]()
            self.super_admin_menu()

        elif choice == 14:
            callToAction[options[choice - 1]]()
        elif choice == 15:
            callToAction[options[choice - 1]]()
            self.super_admin_menu()
        elif choice == 16:
            callToAction[options[choice - 1]]()
        else:
            Exceptions.bad_error()
            Helper().stop_app()


    # TODO NIELS: menu kan vervangen worden door menus(Role.SYSTEM_ADMINISTATOR)

    def system_administator_menu(self):
        callToAction = {
            "List of users": PersonCRUD().checkUsers,
            'Check member': PersonCRUD().search_person,
            'add member': PersonCRUD().addPerson,
            'Modify member': PersonCRUD().modify_person,
            'Delete member': PersonCRUD().delete_person,
            'add a new advisor': PersonCRUD().addPerson,
            'Modify advisor': PersonCRUD().modify_person,
            'Delete advisor': PersonCRUD().delete_person,
            "change password": PersonCRUD().changePassword,
            "make a backup": Helper().make_backup,
            "see log(s)": Helper().see_logs,
            "Logout": UserInterface().main_screen
        }

        options = list(callToAction.keys())
        choice = self.choices(options)
        if choice in [1, 2, 3, 4, 5]:
            PersonCRUD().search_person("member")
            self.super_admin_menu()

        elif choice in [6, 7, 8]:
            PersonCRUD().search_person("advisor")
            self.super_admin_menu()

        elif choice == 9:
            PersonCRUD().changePassword("systemadmin")
            self.super_admin_menu()
        elif choice == 10:
            Helper().make_backup()
        elif choice == 11:
            Helper().see_logs()
            self.super_admin_menu()
        elif choice == 12:
            UserInterface().main_screen()
        else:
            Exceptions.bad_error()
            Helper().stop_app()


    # TODO NIELS: menu kan vervangen worden door menus(Role.ADVISOR)
    def advisor_menu(self):
        callToAction = {
            'Check member': PersonCRUD().search_person,
            'add member': PersonCRUD().addPerson,
            'Modify member': PersonCRUD().modify_person,
            "change password for advisor": PersonCRUD().changePassword,
            "Logout": UserInterface().main_screen
        }
        options = list(callToAction.keys())
        choice = self.choices(options)

        kind = options[choice - 1].split()[-1]
        if choice in [1, 2, 3, 4]:
            callToAction[options[choice - 1]](kind)
            self.advisor_menu()

        elif choice == 5:
            self.login_screen()
        else:
            Exceptions.bad_error()
            Helper().stop_app()
