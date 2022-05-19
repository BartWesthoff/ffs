import sqlite3

from src.cdms.clientClass import Client


class Database:
    def __init__(self, name=None):
        self.conn = None
        self.cursor = None
        if name:
            self.open(name)

    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")
            print(e)

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


    def login(self, kind, username, password):
        query = f"SELECT * FROM {kind} WHERE username = ? AND password = ?;"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()

    def get(self, table, columns, limit=None, where=1):

        # TODO
        # table werkt niet met ? maar is niet erg omdat dit altijd vast staat
        # * werkt ook niet met *
        query = "SELECT ? from ? WHERE ?"
        query2 = f"SELECT * from {table} WHERE ?"
        # database.get(columns='*', table=_type)
        args = (columns, table, where)
        # print(query)
        self.cursor.execute(query2, (where,))
        """
        import datetime
        from cdms.helperClass import Helper
        username = Helper().checkLoggedIn()
        datetime = datetime.datetime.now().strftime("%a %w %b %Y")
        description = "data has been requested"
        suspicous = "no"
        self.cursor.execute(f"Logging", '`username`, `datetime`, `description`, `suspicious`',
                            f"'{username}', '{datetime}', '{description}', '{suspicous}'")
        # fetch data
        """
        rows = self.cursor.fetchall()
        return rows[len(rows) - limit if limit else 0:]

    def getLast(self, table, columns):

        return self.get(table, columns, limit=1)[0]

    def createEmployee(self, kind, firstname, lastname, username, password):
        self.cursor.execute(f"INSERT INTO {kind} VALUES (:id, :first,:last,:user,:pass)",
                            {"id": None, "first": firstname, "last": lastname, "user": username,
                             "pass": password})
        self.commit()


    def createClient(self, client: Client):
        self.cursor.execute(f"INSERT INTO client (firstname,lastname,streetname,housenumber,zipcode,city,emailaddress,mobilephone)VALUES (:first, :last,:street,:house,:zip,:city,:email,:mobile)",
                            {"first": client.firstname, "last": client.lastname, "street": client.street, "house": client.housenumber, "zip": client.zipcode, "city": client.city, "email": client.mail, "mobile": client.mobile_number})


        self.commit()

    def write(self, table, columns="", data=""):
        columns = ("firstname",)
        data = ("WesthoffTest",)

        self.cursor.execute(f'INSERT INTO {table} (?) VALUES (?)', ("firstname", "WesthoffTest"))
        # args = (columns, data)
        """
        import datetime
        from cdms.helperClass import Helper
        username = Helper().checkLoggedIn()
        datetime = datetime.datetime.now().strftime("%a %w %b %Y")
        description = "data has been added"
        suspicous = "yes"
        self.cursor.execute(f"Logging", '`username`, `datetime`, `description`, `suspicious`',
                            f"'{username}', '{datetime}', '{description}', '{suspicous}'")
        """
        # self.cursor.execute(query, [columns[0], data[0]])
        self.commit()

    def delete(self, table, colums, data):

        query = "DELETE FROM ? WHERE id = ? ;", (table, data)
        """
        import datetime
        from cdms.helperClass import Helper
        username = Helper().checkLoggedIn()
        datetime = datetime.datetime.now().strftime("%a %w %b %Y")
        description = "data has been deleted"
        suspicous = "yes"
        self.cursor.execute(f"Logging", '`username`, `datetime`, `description`, `suspicious`',
                            f"'{username}', '{datetime}', '{description}', '{suspicous}'")
        """
        self.cursor.execute(query)

    def updatePassword(self, table, password, id):

        try:
            query = "UPDATE ? SET password = ? WHERE id = ?;", (table, password, id)
            self.cursor.execute(query)
            """
            import datetime
            from cdms.helperClass import Helper
            username = Helper().checkLoggedIn()
            datetime = datetime.datetime.now().strftime("%a %w %b %Y")
            description = f"{username} password has been updated"
            suspicous = "yes"
            self.cursor.execute(f"Logging", '`username`, `datetime`, `description`, `suspicious`',
                                f"'{username}', '{datetime}', '{description}', '{suspicous}'")
            """
        except:
            print("something went wrong")

    def query(self, sql, values=None):
        if values is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, values)
        # self.conn.commit()

    # Check if all required tables are avalible
    def checkMigrations(self):

        try:
            self.query(
                "CREATE TABLE 'systemadmin' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT NULL)")
        except:
            pass
        try:
            self.query(
                "CREATE TABLE 'advisor' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT NULL)")
        except:
            pass
        try:
            self.query(
                "CREATE TABLE 'client' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, 'lastname' VARCHAR(128) NOT NULL, 'streetname' VARCHAR(128) NOT NULL, 'housenumber' INTEGER NOT NULL, 'zipcode' VARCHAR(128) NOT NULL, 'city' VARCHAR(128) NOT NULL, 'emailaddress' VARCHAR(128) NOT NULL, 'mobilephone' VARCHAR(128) NOT NULL)")
        except:
            pass
        try:
            self.query(
                "CREATE TABLE 'superadmin' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT NULL)")
        except:
            pass
        try:
            self.query(
                "CREATE TABLE 'Logging' ('number' INTEGER PRIMARY KEY AUTOINCREMENT, 'username' VARCHAR(128) NOT NULL, 'datetime' VARCHAR(128) NOT NULL, 'description' VARCHAR(128) NOT NULL, 'suspicious' VARCHAR(128) NOT NULL)")
        except:
            pass
        self.open("analyse.db")
        self.commit()
