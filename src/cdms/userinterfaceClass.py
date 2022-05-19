from src.cdms.databaseclass import Database
from src.cdms.helperClass import Helper
from src.cdms.personCrudClass import PersonCRUD


class userinterface:
    def __init__(self):
        pass

    def mainscreen(self):
        database = Database("analyse.db")
        database.checkMigrations()
        database.close()

        choice = self.choices(["Login", "Exit application"], "Which option do you want to choose?: ")
        if choice == 1:
            self.loginscreen()
        elif choice == 2:
            Helper().stopApp()
        else:
            print("Incorrect input, try again.")
            self.mainscreen()

    def loginscreen(self):

        global loginusername, loginpassword
        choice = self.choices(["advisor", "System administrators", "Super administrator"],
                              "What type of user is logging in?: ")

        print(choice)
        _type = None
        if choice == 1:
            _type = 'advisors'
        elif choice == 2:
            _type = 'Systemadmins'
        elif choice == 3:
            _type = 'Superadmin'
        else:
            print("Incorrect input, try again.")
            self.loginscreen()
        loop = True
        count = 0
        loginusername = ""
        loginpassword = ""
        data = ""
        while loop:

            loginusername = input("What is your username?: ")
            loginpassword = input("What is your password?: ")
            # if loginpassword == "Admin321!" and loginusername == "superadmin":
            if loginpassword == "" and loginpassword == "":
                break
            loginusername = Helper().Encrypt(loginusername)
            loginpassword = Helper().Encrypt(loginpassword)
            database = Database("analyse.db")

            try:
                data = database.get(columns='*', table=f'{_type}',
                                    where=f"`username`='{loginusername}' AND `password`='{loginpassword}'")
            except:
                print("Username or password not correct! try again")
            for row in data:
                if row[3] == loginusername and row[4] == loginpassword:
                    loop = False
                    count = 1
            if count == 0:
                print("Wrong username or password, try again.\n")
                loop = True
        Helper().logUsername(loginusername)
        if _type == "advisors":
            self.advisormenu()
        if _type == "Systemadmins":
            self.systemadministatormenu()
        if _type == "Superadmin":
            self.superadminmenu()

    def choices(self, choices, question):
        index = 0
        while index < len(choices):
            print(f"{index + 1}. {choices[index]}")
            index += 1
        c = input(question)
        if c.isnumeric() and len(choices) >= int(c) > 0:

            return int(c)
        else:
            self.choices(choices, question)

    def superadminmenu(self):
        choice = self.choices(
            ["List of users", "Check client", "add client", "Modify client",
             "Delete client",
             "add a new advisor", "Modify advisor", "Delete advisor", "add new systemadmin",
             "change passwords", "make a backup", "see log(s)", "Logout"],
            "Wich option do you want to choose?: ")
        print(choice)
        print(type(choice))
        if choice == 1:
            PersonCRUD().checkUsers("Clients")
            self.superadminmenu()
        elif choice == 2:
            PersonCRUD().searchPerson("Clients")
            self.superadminmenu()

        elif choice == 3:
            PersonCRUD().addPerson("Clients")
            self.superadminmenu()

        elif choice == 4:
            PersonCRUD().modifyPerson("Clients")
            self.superadminmenu()
        elif choice == 5:
            PersonCRUD().deletePerson("Clients")
            self.superadminmenu()
        elif choice == 6:
            print("went into adding a advisor")
            PersonCRUD().addPerson("Advisors")
            self.superadminmenu()
        elif choice == 7:
            PersonCRUD().modifyPerson("Advisors")
            self.superadminmenu()
        elif choice == 8:
            PersonCRUD().deletePerson("Advisors")
            self.superadminmenu()

        elif choice == 9:
            PersonCRUD().addPerson("Systemadmins")
            self.superadminmenu()
        elif choice == 10:
            PersonCRUD().changePassword("Superadmin")
            self.superadminmenu()
        elif choice == 11:
            Helper().makeBackup()
        elif choice == 12:
            print("see logs init")
            Helper().seelogs()
            self.superadminmenu()
        elif choice == 13:
            userinterface().mainscreen()
        else:
            print("Wrong input, try again.")
            self.superadminmenu()
    #
    # def superadminmenu(self):
    #     choice = self.choices(
    #         ["List of users", "Check client", "add client", "Modify client",
    #          "Delete client",
    #          "add a new advisor", "Modify advisor", "Delete advisor", "add new systemadmin",
    #          "change passwords", "make a backup", "see log(s)", "Logout"],
    #         "Wich option do you want to choose?: ")
    #
    #     if choice == 1:
    #         PersonCRUD().checkUsers("Clients")
    #
    #     elif choice == 2:
    #         PersonCRUD().searchPerson("Clients")
    #
    #     elif choice == 3:
    #         PersonCRUD().addPerson("Clients")
    #
    #     elif choice == 4:
    #         PersonCRUD().modifyPerson("Clients")
    #
    #     elif choice == 5:
    #         PersonCRUD().deletePerson("Clients")
    #
    #     elif choice == 6:
    #         print(choice)
    #         PersonCRUD().addPerson("advisors")
    #
    #     elif choice == 7:
    #         PersonCRUD().modifyPerson("advisors")
    #
    #     elif choice == 8:
    #         PersonCRUD().deletePerson("advisors")
    #
    #     elif choice == 9:
    #         PersonCRUD().addPerson("Systemadmins")
    #
    #     elif choice == 10:
    #         PersonCRUD().changePassword("Superadmin")
    #
    #     elif choice == 11:
    #         Helper().makeBackup()
    #     elif choice == 12:
    #         print("see logs init")
    #         Helper().seelogs()
    #
    #     elif choice == 13:
    #         userinterface().mainscreen()
    #
    #     else:
    #         print("Wrong input, try again.")
    #         self.superadminmenu()
    #
    #     if choice in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
    #         self.superadminmenu()

    # def systemadministatormenu(self):
    #     choice = self.choices(
    #         ["List of users", "Check client", "add client", "Modify client",
    #          "Delete client",
    #          "add a new advisor", "Modify advisor", "Delete advisor",
    #          "Change passwords", "make a backup", "see log(s)", "Logout"],
    #         "Wich option do you want to choose?: ")
    #     if choice == 1:
    #         pass
    #     elif choice == 2:
    #         PersonCRUD().searchPerson("Clients")
    #         self.superadminmenu()
    #
    #     elif choice == 3:
    #         PersonCRUD().addPerson("Clients")
    #         self.superadminmenu()
    #
    #     elif choice == 4:
    #         PersonCRUD().modifyPerson("Clients")
    #         self.superadminmenu()
    #     elif choice == 5:
    #         PersonCRUD().deletePerson("Clients")
    #         self.superadminmenu()
    #     elif choice == 6:
    #         PersonCRUD().addPerson("advisors")
    #         self.superadminmenu()
    #     elif choice == 7:
    #         PersonCRUD().modifyPerson("advisors")
    #         self.superadminmenu()
    #     elif choice == 8:
    #         PersonCRUD().deletePerson("advisors")
    #         self.superadminmenu()
    #
    #     elif choice == 9:
    #         PersonCRUD().changePassword("Systemadmins")
    #         self.superadminmenu()
    #     elif choice == 10:
    #         Helper().makeBackup()
    #     elif choice == 11:
    #         Helper().seelogs()
    #         self.superadminmenu()
    #     elif choice == 12:
    #         userinterface().mainscreen()
    #     else:
    #         print("Wrong input, try again.")
    #         self.systemadministatormenu()

    def systemadministatormenu(self):
        choice = self.choices(
            ["List of users", "Check client", "add client", "Modify client",
             "Delete client",
             "add a new advisor", "Modify advisor", "Delete advisor",
             "Change passwords", "make a backup", "see log(s)", "Logout"],
            "Wich option do you want to choose?: ")
        if choice == 1:
            pass
        elif choice == 2:
            PersonCRUD().searchPerson("Clients")

        elif choice == 3:
            PersonCRUD().addPerson("Clients")

        elif choice == 4:
            PersonCRUD().modifyPerson("Clients")

        elif choice == 5:
            PersonCRUD().deletePerson("Clients")

        elif choice == 6:
            PersonCRUD().addPerson("advisors")

        elif choice == 7:
            PersonCRUD().modifyPerson("advisors")

        elif choice == 8:
            PersonCRUD().deletePerson("advisors")

        elif choice == 9:
            PersonCRUD().changePassword("Systemadmins")

        elif choice == 10:
            Helper().makeBackup()

        elif choice == 11:
            Helper().seelogs()

        elif choice == 12:
            userinterface().mainscreen()

        else:
            print("Wrong input, try again.")
            self.systemadministatormenu()

        if choice in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]:
            self.superadminmenu()

    def advisormenu(self):
        choice = self.choices(
            ["add client | works", "Modify client", "Search client",
             "Reset your password",
             "Logout"],
            "Wich option do you want to choose?: ")
        if choice == 1:
            PersonCRUD().addPerson("Clients")

        elif choice == 2:
            PersonCRUD().modifyPerson("Clients")

        elif choice == 3:
            PersonCRUD().searchPerson("Clients")

        elif choice == 4:
            PersonCRUD().changePassword("advisors")

        elif choice == 5:
            self.loginscreen()
        else:
            print("Wrong input, try again.")

        if choice in [1, 2, 3, 4]:
            self.advisormenu()
