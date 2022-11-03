import json
import re
from random import randint
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
        # TODO: REPLACE alphabet_upper = alphabet.upper()
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




    @staticmethod
    def generate_uuid():
        # TODO: checken of id niet in database zit
        uuid = [str(randint(0 if i == 0 else 1, 9)) for i in range(9)]
        last_digit = sum(int(i) for i in uuid) % 10
        return ''.join(uuid) + str(last_digit)
    @staticmethod
    def username_checker(username):
        from cdms.databaseclass import Database
        database = Database("analyse.db")
        while True:
            test = 0
            dataAdvisor = database.get_all_of_kind(kind='advisor')
            dataSystemAdmin = database.get_all_of_kind(kind='systemadmin')

            database.commit()

            for ch in username:
                if ch[0].isalpha():
                    test += 1
                break

            if 6 <= len(username) < 10:
                test += 1
            
            for row in dataAdvisor:
                if Helper().decrypt(row[3]) == username:
                    test += 1

            for row in dataSystemAdmin:
                if Helper().decrypt(row[3]) == username:
                    test += 1

            if test == 2:
                break
            print(test)
            username = input('Please enter correct username, name needs to be unique, between 6 and 10 characters and start with an letter : ')
        return username

    @staticmethod
    # TODO: ENCRYPT/DECRYPT USERNAME
    def log_username(username):
        _dict = {"username": username}
        with open("username.json", "w+") as f:
            json.dump(_dict, f)

    # TODO: ENCRYPT/DECRYPT USERNAME
    @staticmethod
    def check_logged_in():
        with open("username.json", "r") as f:
            _dict = json.load(f)
        return _dict["username"]

    @staticmethod
    def make_backup():
        # TODO low: Circular import vermijden
        from cdms.databaseclass import Database

        database = Database("analyse.db")
        database.add_log(description="database backup", suspicious="no")

        copyfile('analyse.db', 'analyse_backup.db')

    @staticmethod
    def restore_backup():
        # TODO low: Circular import vermijden
        from cdms.databaseclass import Database

        database = Database("analyse_backup.db")
        # because it's filling in first then backing up with the already logged case
        database.add_log(description="database restore", suspicious="no")
        copyfile('analyse_backup.db', 'analyse.db')

    @staticmethod
    def see_logs():
        # TODO low: Circular import vermijden
        from cdms.databaseclass import Database
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


        # TODO: Goede exception handling
        except Exception as e:
            print("logs not found, try again")

        database.close()
