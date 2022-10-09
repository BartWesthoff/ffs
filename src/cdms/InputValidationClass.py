import re



class Validator:

    def is_valid_number(self, number):
        from src.cdms.databaseclass import Database
        if not number.isnumeric():
            number = input("Must be a number, try again: ")
            database = Database("analyse.db")
            database.add_log(
                    description=f"Input not a valid number.",
                    suspicious="no")
            self.is_valid_number(number)
        return int(number)

    def is_valid_zipcode(self, zipcode):
        from src.cdms.databaseclass import Database
        if not zipcode[0:3].isnumeric():
            database = Database("analyse.db")
            zipcode = input("Please enter a valid zipcode, try again: ")
            database.add_log(
                    description=f"Zip code not valid.",
                    suspicious="no")
            self.is_valid_zipcode(zipcode)
        if not zipcode[4:5].isalpha():
            
            zipcode = input("Please enter a valid zipcode, try again: ")
            database = Database("analyse.db")
            database.add_log(
                    description=f"Zip code not valid.",
                    suspicious="no")
            self.is_valid_zipcode(zipcode)
        if len(zipcode) != 6:
            zipcode = input("Please enter a valid zipcode, try again: ")
            database = Database("analyse.db")
            database.add_log(
                    description=f"Zip code not valid.",
                    suspicious="no")
            self.is_valid_zipcode(zipcode)

        # TODO: REPLACE   of error codes specifiek maken
        # if not zipcode[0:3].isnumeric() or not zipcode[4:5].isalpha() or len(zipcode) != 6:
        #     zipcode = input("Please enter a valid zipcode, try again: ")
        #     self.is_valid_zipcode(zipcode)
        return zipcode.capitalize()

    def is_valid_name(self, name):
        from src.cdms.databaseclass import Database
        if not name.isalpha():
            name = input("name cannot include a integer. Try again: ")
            database = Database("analyse.db")
            
            database.add_log(
                    description=f"Wrong input for name.",
                    suspicious="no")
            self.is_valid_name(name)
        if len(name) > 20:
            name = input("name cannot be a longer than 20 characters. Try again: ")
            database = Database("analyse.db")
            database.add_log(
                    description=f"Name is too long.",
                    suspicious="no")
            self.is_valid_name(name)

        return name.capitalize()

    def is_valid_email(self, email):
        from src.cdms.databaseclass import Database
        valid_email = re.search(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
        if not valid_email:
            email = input("Please enter a valid email: ")
            database = Database("analyse.db")
            database.add_log(
                    description=f"Email is not valid.",
                    suspicious="no")
            self.is_valid_email(email)
        return email.lower()

    def is_valid_phone_number(self, number):
        from src.cdms.databaseclass import Database
        # TODO Specifieke error codes
        if not number.isnumeric() or len(number) != 8:
            number = input("Please enter a valid number: ")
            database = Database("analyse.db")
            database.add_log(
                    description=f"Phone number is not valid",
                    suspicious="no")
            self.is_valid_phone_number(number)
        return number
