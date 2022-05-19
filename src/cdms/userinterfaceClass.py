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

        choice = self.choices(["Login", "Exit application"])
        if choice == 1:
            self.loginscreen()
        elif choice == 2:
            Helper().stopApp()
        else:
            print("Incorrect input, try again.")
            self.mainscreen()

    def loginscreen(self):

        global loginusername, loginpassword
        choice = self.choices(["advisor", "System administrators", "Super administrator"])

        print(choice)
        _type = None
        if choice == 1:
            _type = "advisor"
        elif choice == 2:
            _type = "systemadmin"
        elif choice == 3:
            _type = "superadmin"
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
                print(loginusername)
                print(loginpassword)
                print(_type)
                data = database.login(kind=f'{_type}', username=loginusername, password=loginpassword)
                if data is not None:
                    break


            except:
                print("Username or password not correct! try again")
                print(data)
            print(data)

        Helper().logUsername(loginusername)
        if _type == "advisor":
            self.advisormenu()
        if _type == "systemadmin":
            self.systemadministatormenu()
        if _type == "superadmin":
            self.superadminmenu()

    def choices(self, choices, question="Which option do you want to choose?: "):
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
        callToAction = {
            "List of users": PersonCRUD().checkUsers,
            'Check client': PersonCRUD().searchPerson,
            'add client': PersonCRUD().addPerson,
            'Modify client': PersonCRUD().modifyPerson,
            'Delete client': PersonCRUD().deletePerson,
            'add a new advisor': PersonCRUD().addPerson,
            'Modify advisor': PersonCRUD().modifyPerson,
            'Delete advisor': PersonCRUD().deletePerson,
            "add a new system administrator": PersonCRUD().addPerson,  # new from previous inheritance
            "change password": PersonCRUD().changePassword,  # check if from existing employee
            "make a backup": Helper().makeBackup,
            "see log(s)": Helper().seelogs,
            "Logout": userinterface().mainscreen

            # TODO create Restore backup
        }
        options = list(callToAction.keys())
        choice = self.choices(options)
        # if choice == 1:
        #     callToAction[options[choice - 1]]()
        #     self.superadminmenu()
        # elif choice == 2:
        #     callToAction[options[choice - 1]]("client")
        #     self.superadminmenu()
        #
        # elif choice == 3:
        #     callToAction[options[choice - 1]]("client")
        #     self.superadminmenu()
        #
        # elif choice == 4:
        #     callToAction[options[choice - 1]]("client")
        #     self.superadminmenu()
        # elif choice == 5:
        #     callToAction[options[choice - 1]]("client")
        #     self.superadminmenu()

        if choice in [1, 2, 3, 4, 5]:
            callToAction[options[choice - 1]]("client")
            self.superadminmenu()

        # elif choice == 6:
        #     print("went into adding a advisor")
        #     callToAction[options[choice - 1]]("advisor")
        #     self.superadminmenu()
        # elif choice == 7:
        #     callToAction[options[choice - 1]]("advisor")
        #     self.superadminmenu()
        # elif choice == 8:
        #     callToAction[options[choice - 1]]("advisor")
        #     self.superadminmenu()

        elif choice in [6, 7, 8]:
            callToAction[options[choice - 1]]("advisor")
            self.superadminmenu()

        elif choice == 9:
            callToAction[options[choice - 1]]("systemadmin")
            self.superadminmenu()
        elif choice == 10:
            callToAction[options[choice - 1]]("superadmin")
            self.superadminmenu()

        elif choice == 11:
            callToAction[options[choice - 1]]()
        elif choice == 12:
            callToAction[options[choice - 1]]()
            self.superadminmenu()
        elif choice == 13:
            callToAction[options[choice - 1]]()
        else:
            print("Wrong input, try again.")
            self.superadminmenu()

    def systemadministatormenu(self):
        callToAction = {
            "List of users": PersonCRUD().checkUsers,
            'Check client': PersonCRUD().searchPerson,
            'add client': PersonCRUD().addPerson,
            'Modify client': PersonCRUD().modifyPerson,
            'Delete client': PersonCRUD().deletePerson,
            'add a new advisor': PersonCRUD().addPerson,
            'Modify advisor': PersonCRUD().modifyPerson,
            'Delete advisor': PersonCRUD().deletePerson,
            "change password": PersonCRUD().changePassword,
            "make a backup": Helper().makeBackup,
            "see log(s)": Helper().seelogs,
            "Logout": userinterface().mainscreen

            ## TODO To reset an existing advisor’s password (a temporary password)
        }

        options = list(callToAction.keys())
        choice = self.choices(options)
        # if choice == 1:
        #     pass
        # elif choice == 2:
        #     PersonCRUD().searchPerson("client")
        #     self.superadminmenu()
        #
        # elif choice == 3:
        #     PersonCRUD().addPerson("client")
        #     self.superadminmenu()
        #
        # elif choice == 4:
        #     PersonCRUD().modifyPerson("client")
        #     self.superadminmenu()
        # elif choice == 5:
        #     PersonCRUD().deletePerson("client")
        #     self.superadminmenu()

        if choice in [1, 2, 3, 4, 5]:
            PersonCRUD().searchPerson("client")
            self.superadminmenu()

        # elif choice == 6:
        #     PersonCRUD().addPerson("advisor")
        #     self.superadminmenu()
        # elif choice == 7:
        #     PersonCRUD().modifyPerson("advisor")
        #     self.superadminmenu()
        # elif choice == 8:
        #     PersonCRUD().deletePerson("advisor")
        #     self.superadminmenu()
        elif choice in [6, 7, 8]:
            PersonCRUD().searchPerson("advisor")
            self.superadminmenu()

        elif choice == 9:
            PersonCRUD().changePassword("systemadmin")
            self.superadminmenu()
        elif choice == 10:
            Helper().makeBackup()
        elif choice == 11:
            Helper().seelogs()
            self.superadminmenu()
        elif choice == 12:
            userinterface().mainscreen()
        else:
            print("Wrong input, try again.")
            self.systemadministatormenu()

    def advisormenu(self):
        callToAction = {
            'Check client': PersonCRUD().searchPerson,
            'add client': PersonCRUD().addPerson,
            'Modify client': PersonCRUD().modifyPerson,
            "change password": PersonCRUD().changePassword,
            "Logout": userinterface().mainscreen
        }
        options = list(callToAction.keys())
        choice = self.choices(options)

        kind = options[choice - 1].split()[-1]
        if choice in [1, 2, 3, 4]:
            callToAction[options[choice - 1]](kind)
            self.advisormenu()

        elif choice == 5:
            self.loginscreen()
        else:
            print("Wrong input, try again.")
