import json
import re
from shutil import copyfile



class Helper:

    @staticmethod
    def stop_app():
        quit()

    @staticmethod
    def encrypt(text):
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
    def decrypt(text):
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

    def password_checker(self, password):
        x = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$", password)
        error = '''\n Please enter correct password. Min length of 8, no longer than 30 characters, 
        MUST have at least one lowercase letter, one uppercase letter, one digit and one special character :'''
        if not x:
            password = input(error)
            self.password_checker(password)
        else:
            print('\n Password is accepted.')
            return password

    @staticmethod
    def username_checker(username):
        while len(username) < 5 or len(username) > 10:
            username = input('Please enter correct username, name needs to be between 5 and 10 characters : ')
        return username

    @staticmethod
    def is_valid_number(input):
        return input.isnumeric()

    @staticmethod
    def log_username(username):
        _dict = {"username": username}
        with open("username.json", "w+") as f:
            json.dump(_dict, f)

    @staticmethod
    def check_logged_in():
        with open("username.json", "r") as f:
            _dict = json.load(f)
        return _dict["username"]

    @staticmethod
    def make_backup():
        from src.cdms.databaseclass import Database

        database = Database("analyse.db")
        database.add_log(description="database backup", suspicious="no")

        copyfile('analyse.db', 'analyse_backup.db')

    @staticmethod
    def restore_backup():
        from src.cdms.databaseclass import Database

        database = Database("analyse_backup.db")
        # because its filling in first then backing up with the already logged case
        database.add_log(description="database restore", suspicious="no")
        copyfile('analyse_backup.db', 'analyse.db')

    @staticmethod
    def see_logs():
        from src.cdms.databaseclass import Database
        database = Database("analyse.db")
        kind = "logging"
        data = database.get(columns='*', table=f'{kind}')
        database.commit()
        try:
            for row in data:
                print("ID             |", row[0])
                print("Username       |", Helper().decrypt(row[1]))
                print("Date           |", row[2])
                print("Description    |", Helper().decrypt(row[3]))
                print("suspicious     |", Helper().decrypt(row[4]), "\n")


        except:
            print("logs not found, try again")

        database.close()
