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
        key = 4
        decrypted_message = ""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alphabet_upper = "abcdefghijklmnopqrstuvwxyz".upper()
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
            else:
                decrypted_message += c
        return decrypted_message

    @staticmethod
    def Decrypt(text):

        print("text to be decripted: " + text)
        key = 4
        decrypted_message = ""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alphabet_upper = "abcdefghijklmnopqrstuvwxyz".upper()
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
        while len(username) < 5 or len(username) > 20:
            username = input('\n Please enter correct username, name needs to be between 5 and 20 characters : ')
        return username

    @staticmethod
    def makeBackup():
        conn = sqlite3.connect('analyse.db')

        # Open() function
        with io.open('analyse_backup.sql', 'w') as p:
            # iterdump() function
            for line in conn.iterdump():
                p.write('%s\n' % line)

        print('Backup performed successfully!')
        print('Data Saved as backupdatabase_dump.sql')

        conn.close()

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

    @staticmethod
    def seelogs():
        from src.cdms.databaseclass import Database
        print("went in function")
        database = Database("analyse.db")
        kind = "Logging"
        data = database.get(columns='*', table=f'{kind}')
        database.commit()
        print(data)
        try:
            for row in data:
                print("ID             |", row[0])
                print("Username       |", Helper().Decrypt(row[1]))
                print("Date           |", row[2])
                print("Description    |", Helper().Decrypt(row[3]))
                print("Additional info|", "nog implementeren")
                print("suspicious     |", Helper().Decrypt(row[4]), "\n")


        except:
            print("Person not found, try again")

        database.close()
