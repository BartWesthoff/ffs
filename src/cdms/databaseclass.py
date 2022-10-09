import datetime
import sqlite3
from src.cdms.memberClass import Member
from src.cdms.helperClass import Helper


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

    def login(self, kind: str, username: str, password: str):
        query = f"SELECT * FROM {kind} WHERE username = ? AND password = ?;"
        print(f"SELECT * FROM {kind} WHERE username = {username} AND password = {password};")
        self.cursor.execute(query, (username, password))

        result = self.cursor.fetchone()
        if result is None:
            return False
        return result

    def search_employee(self, kind, firstname, lastname, username):
        query = f"SELECT * FROM {kind} WHERE firstname = ? AND lastname = ? AND username = ? ;"

        print(f"SELECT * FROM {kind} WHERE firstname = {firstname} AND lastname = {lastname} and username {username};")

        self.cursor.execute(query, (firstname, lastname, username))

        return self.cursor.fetchone()

    def search_person(self, kind, firstname, lastname):
        query = f"SELECT * FROM {kind} WHERE firstname = ? AND lastname = ?;"

        print(f"SELECT * FROM {kind} WHERE firstname = {firstname} AND lastname = {lastname};")

        self.cursor.execute(query, (firstname, lastname))

        return self.cursor.fetchone()

    def search_person_by_id(self, kind, id):
        query = f"SELECT * FROM {kind} WHERE id = ?;"
        print(f"SELECT * FROM {kind} WHERE id = {id};")
        self.cursor.execute(query, id)
        return self.cursor.fetchone()

    def get_all_of_kind(self, kind):
        query = f"SELECT * FROM {kind};"
        print(f"SELECT * FROM {kind};")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_log(self, description, suspicious):

        username = Helper().check_logged_in()
        username = Helper().encrypt(username)
        description = Helper().encrypt(description)
        suspicious = Helper().encrypt(suspicious)
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.cursor.execute(
            f"INSERT INTO logging (username,datetime,description,suspicious)VALUES (:user, :date,:desc,:sus)",
            {"user": username, "date": now, "desc": description, "sus": suspicious})
        print(
            f"INSERT INTO logging (username,datetime,description,suspicious)VALUES ({username}, {now},{description},{suspicious})")
        self.commit()

    def get(self, table, columns, limit=None, where=1):

        query2 = f"SELECT * from {table} WHERE ?"
        print(f"SELECT * from {table} WHERE {where}")
        args = (columns, table, where)
        self.cursor.execute(query2, (where,))

        rows = self.cursor.fetchall()
        return rows[len(rows) - limit if limit else 0:]

    def get_last(self, table, columns):

        return self.get(table, columns, limit=1)[0]

    def create_employee(self, kind, firstname, lastname, username, password, registration_date, id):

        print(f"INSERT INTO {kind} VALUES ({id}, {firstname}, {lastname}, {username}, {password}, {registration_date})")

        self.cursor.execute(f"INSERT INTO {kind} VALUES (:id, :first,:last,:user,:pass,:date)",
                            {"id": id, "first": firstname, "last": lastname, "user": username,
                             "pass": password, "date": registration_date})
        self.commit()

    def create_member(self, member: Member):
        self.cursor.execute(
            "INSERT INTO member VALUES (:id, :first,:last,:email,:street,:house_number, :zipcode, :city, :phone, :date)",
            {"id": member.id, "first": member.firstname, "last": member.lastname, "email": member.mail,
                "street": member.street, "house_number": member.house_number, "zipcode": member.zipcode,
                "city": member.city, "phone": member.mobile_number, "date": member.registration_date})
        self.commit()

    def delete_employee(self, table, firstname, lastname, username):

        query = f"DELETE FROM {table} WHERE firstname = ? AND lastname = ? AND username = ? ;"
        print(f"DELETE FROM {table} WHERE firstname = {firstname} AND lastname = {lastname} AND username = {lastname};")
        args = (firstname, lastname, username)
        self.cursor.execute(query, args)

    def delete_person(self, table, firstname, lastname):

        query = f"DELETE FROM {table} WHERE firstname = ? AND lastname = ?;"
        print(f"DELETE FROM {table} WHERE firstname = {firstname} AND lastname = {lastname};")
        args = (firstname, lastname)
        self.cursor.execute(query, args)

    def update_password(self, kind, password, username):
        print(f"UPDATE {kind} SET password = ? WHERE username = ?;", (password, username))
        self.cursor.execute(f"UPDATE {kind} SET password = ? WHERE username = ?;", (password, username))

    def query(self, sql, values=None):
        if values is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, values)

    def check_migrations(self):

        try:
            self.query(
                "CREATE TABLE 'systemadmin' ('id' INTEGER PRIMARY KEY NOT NULL, 'firstname' VARCHAR(128) NOT "
                "NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'date' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) "
                "NOT NULL)")

            self.query(
                "CREATE TABLE 'advisor' ('id' INTEGER PRIMARY KEY NOT NULL, 'firstname' VARCHAR(128) NOT NULL, "
                "'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'date' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT "
                "NULL)")

            self.query(
                "CREATE TABLE 'member' ('id' INTEGER PRIMARY KEY NOT NULL, 'firstname' VARCHAR(128) NOT NULL, "
                "'lastname' VARCHAR(128) NOT NULL, 'streetname' VARCHAR(128) NOT NULL, 'housenumber' INTEGER NOT "
                "NULL, 'zipcode' VARCHAR(128) NOT NULL, 'city' VARCHAR(128) NOT NULL, 'emailaddress' VARCHAR(128) NOT "
                "NULL, 'mobilephone' VARCHAR(128) NOT NULL, 'date' VARCHAR(128) NOT NULL)")

            self.query(
                "CREATE TABLE 'superadmin' ('id' INTEGER PRIMARY KEY NOT NULL, 'firstname' VARCHAR(128) NOT "
                "NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) "
                "NOT NULL)")

            self.query(
                "CREATE TABLE 'logging' ('number' INTEGER PRIMARY KEY AUTOINCREMENT, 'username' VARCHAR(128) NOT "
                "NULL, 'datetime' VARCHAR(128) NOT NULL, 'description' VARCHAR(128) NOT NULL, 'suspicious' VARCHAR("
                "128) NOT NULL)")
        except:
            Exception("Error while creating tables")
        self.open("analyse.db")
        self.commit()
