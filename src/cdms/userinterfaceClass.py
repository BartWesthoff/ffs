from email import message
from tabnanny import check

from src.cdms.databaseclass import Database
from src.cdms.helperClass import Helper
from src.cdms.messegaClass import Messages
from src.cdms.personCrudClass import PersonCRUD


class userinterface:
    def __init__(self):
        pass

    def mainscreen(self):
        database = Database("analyse.db")
        database.checkMigrations()
        database.close()

        choice: int = self.choices(["Login", "Exit application"])
        if choice == 1:
            self.loginscreen()
        if choice == 2:
            Helper().stopApp()
        else:
            Messages().badError()
            Helper().stopApp()

    def loginscreen(self):
        loop = True
        loginusername = ""
        usernames = []
        passwords = []
        data = ""
        tries = 0
        choice = self.choices(["advisor", "System administrators", "Super administrator"])
        if choice == 1:
            # self.advisormenu()
            _type = "advisor"
        elif choice == 2:
            # self.systemadministatormenu()
            _type = "systemadmin"
        elif choice == 3:
            # self.superadminmenu()
            _type = "superadmin"
        else:
            Messages().badError()
            Helper().stopApp()
            self.loginscreen()

        while loop:
            if tries == 3:
                print("3 wrong tries, incident logged.")
                print([ (user,pw) for user,pw in zip(usernames,passwords)])
                database = Database("analyse.db")
                database.addLog(description=f"3 wrong tries combinations {[ (user,pw) for user,pw in zip(usernames,passwords)]}.", suspicious="yes")
                Helper().stopApp()

            loginusername = input("What is your username?: ")
            loginpassword = input("What is your password?: ")

            passwords.append(loginpassword)
            usernames.append(loginusername)

            if loginpassword == "Admin321!!" and loginusername == "superadmin":
                break

            loginusername = Helper().Encrypt(loginusername)
            loginpassword = Helper().Encrypt(loginpassword)
            database = Database("analyse.db")

            data = database.login(kind=_type, username=loginusername, password=loginpassword)

            if data is False:
                print("Wrong username or password, try again.\n")
                tries += 1
            else:
                break
            # print(data)

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
            print(Messages().wrongNumber())
            self.choices(choices, question)

    def superadminmenu(self):
        callToAction = {
            "List of users": PersonCRUD().checkUsers,
            'Check member': PersonCRUD().searchPerson,
            'add member': PersonCRUD().addPerson,
            'Modify member': PersonCRUD().modifyPerson,
            'Delete member': PersonCRUD().deletePerson,
            'add a new advisor': PersonCRUD().addPerson,
            'Modify advisor': PersonCRUD().modifyPerson,
            'Delete advisor': PersonCRUD().deletePerson,
            "chang password": PersonCRUD().changePassword,
            "add a new system administrator": PersonCRUD().addPerson,
            'Modify system administrator': PersonCRUD().modifyPerson,
            'Delete system administrator': PersonCRUD().deletePerson,  # new from previous inheritance
            "make a backup": Helper().makeBackup,
            "see log(s)": Helper().seelogs,
            "Logout": userinterface().mainscreen

            # TODO create Restore backup
        }
        options = list(callToAction.keys())
        choice = self.choices(options)

        if choice == 1:
            callToAction[options[choice - 1]]()
            self.superadminmenu()
        if choice in [1, 2, 3, 4, 5]:
            callToAction[options[choice - 1]]("member")
            self.superadminmenu()
        elif choice in [6, 7, 8]:
            callToAction[options[choice - 1]]("advisor")
            self.superadminmenu()

        elif choice in [9]:
            callToAction[options[choice - 1]]("superadmin")
            self.superadminmenu()
        elif choice == 10:
            callToAction[options[choice - 1]]("systemadmin")
            self.superadminmenu()
        elif choice == 11:
            callToAction[options[choice - 1]]("systemadmin")
            self.superadminmenu()
        elif choice == 12:
            callToAction[options[choice - 1]]("systemadmin")
            self.superadminmenu()
        elif choice == 13:
            callToAction[options[choice - 1]]("systemadmin")
            self.superadminmenu()

        elif choice == 14:
            callToAction[options[choice - 1]]()
        elif choice == 15:
            callToAction[options[choice - 1]]()
            self.superadminmenu()
        elif choice == 16:
            callToAction[options[choice - 1]]()
        else:
            Messages().badError()
            Helper().stopApp()

    def systemadministatormenu(self):
        callToAction = {
            "List of users": PersonCRUD().checkUsers,
            'Check member': PersonCRUD().searchPerson,
            'add member': PersonCRUD().addPerson,
            'Modify member': PersonCRUD().modifyPerson,
            'Delete member': PersonCRUD().deletePerson,
            'add a new advisor': PersonCRUD().addPerson,
            'Modify advisor': PersonCRUD().modifyPerson,
            'Delete advisor': PersonCRUD().deletePerson,
            "change password": PersonCRUD().changePassword,
            "make a backup": Helper().makeBackup,
            "see log(s)": Helper().seelogs,
            "Logout": userinterface().mainscreen
        }

        options = list(callToAction.keys())
        choice = self.choices(options)
        if choice in [1, 2, 3, 4, 5]:
            PersonCRUD().searchPerson("member")
            self.superadminmenu()

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
            Messages().badError()
            Helper().stopApp()

    def advisormenu(self):
        callToAction = {
            'Check member': PersonCRUD().searchPerson,
            'add member': PersonCRUD().addPerson,
            'Modify member': PersonCRUD().modifyPerson,
            "change password for advisor": PersonCRUD().changePassword,
            "Logout": userinterface().mainscreen
        }
        options = list(callToAction.keys())
        choice = self.choices(options)

        kind = options[choice - 1].split()[-1]
        print(kind)
        if choice in [1, 2, 3, 4]:
            callToAction[options[choice - 1]](kind)
            self.advisormenu()

        elif choice == 5:
            self.loginscreen()
        else:
            Messages().badError()
            Helper().stopApp()
