import datetime
import io
import json
import re
import sqlite3


class Helper:

    @staticmethod
    def stopApp():
        quit()

    @staticmethod
    def Encrypt(text):
        text = str(text)
        key = 4
        decrypted_message = ""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alphabet_upper = "abcdefghijklmnopqrstuvwxyz".upper()
        numbers = "0123456789"

        for c in text:
            if c in alphabet:
                position = alphabet.find(c)
                new_position = (position + key) % 26
                new_character = alphabet[new_position]
                decrypted_message += new_character
            elif c in alphabet_upper:
                position = alphabet_upper.find(c)
                new_position = (position + key) % 26
                new_character = alphabet_upper[new_position]
                decrypted_message += new_character
            elif c in numbers:
                position = numbers.find(c)
                new_position = (position + key) % 10
                new_character = numbers[new_position]
                decrypted_message += new_character
            else:
                decrypted_message += c
        return decrypted_message

    @staticmethod
    def Decrypt(text):
        text = str(text)

        key = 4
        decrypted_message = ""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alphabet_upper = "abcdefghijklmnopqrstuvwxyz".upper()
        numbers = "0123456789"
        for c in text:
            if c in alphabet:
                position = alphabet.find(c)
                new_position = (position - key) % 26
                new_character = alphabet[new_position]
                decrypted_message += new_character
            elif c in alphabet_upper:
                position = alphabet_upper.find(c)
                new_position = (position - key) % 26
                new_character = alphabet_upper[new_position]
                decrypted_message += new_character

            elif c in numbers:
                position = numbers.find(c)
                new_position = (position - key) % 10
                new_character = numbers[new_position]
                decrypted_message += new_character
            else:
                decrypted_message += c
        return decrypted_message

    def passwordchecker(self, password):
        x = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$", password)
        error = '''\n Please enter correct password. Min length of 8, no longer than 30 characters, 
        MUST have at least one lowercase letter, one uppercase letter, one digit and one special character :'''
        if not x:
            password = input(error)
            self.passwordchecker(password)
        else:
            print('\n Password is accepted.')
            return password



    @staticmethod
    def usernameChecker(username):
        while len(username) < 5 or len(username) > 10:
            username = input('Please enter correct username, name needs to be between 5 and 10 characters : ')
        return username

    @staticmethod
    def isValidNumber(input):
        return input.isnumeric()

    @staticmethod
    def logUsername(username):
        _dict = {"username": username}
        with open("username.json", "w+") as f:
            json.dump(_dict, f)

    @staticmethod
    def checkLoggedIn():
        with open("username.json", "r") as f:
            _dict = json.load(f)
        return _dict["username"]

    def makeBackup(self):
        database = Database("analyse.db")
        database.addLog(description="database backup", suspicious="no")

        copyfile('analyse.db', 'analyse_backup.db')

    def restorebackup(self):
        database = Database("analyse_backup.db")
        # because its filling in first then backing up with the already logged case
        database.addLog(description="database restore", suspicious="no")
        copyfile('analyse_backup.db', 'analyse.db')

    @staticmethod
    def seelogs():
        from src.cdms.databaseclass import Database
        database = Database("analyse.db")
        kind = "logging"
        data = database.get(columns='*', table=f'{kind}')
        database.commit()
        try:
            for row in data:
                print("ID             |", row[0])
                print("Username       |", Helper().Decrypt(row[1]))
                print("Date           |", row[2])
                print("Description    |", Helper().Decrypt(row[3]))
                print("suspicious     |", Helper().Decrypt(row[4]), "\n")


        except:
            print("logs not found, try again")

        database.close()
