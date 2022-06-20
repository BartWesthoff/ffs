import datetime
import sqlite3
from ast import arg

from src.cdms.helperClass import Helper
from src.cdms.memberClass import Member


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
        self.cursor.execute(query, (username, password))

        result = self.cursor.fetchone()
        if result is None:
            return False
        return result

    def searchPerson(self, kind, firstname, lastname):
        query = f"SELECT * FROM {kind} WHERE firstname = ? AND lastname = ?;"
        self.cursor.execute(query, (firstname, lastname))
        return self.cursor.fetchone()

    def getAllofKind(self, kind):
        query = f"SELECT * FROM {kind};"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def addLog(self, description, suspicious):

        username = Helper().checkLoggedIn()
        username = Helper().Encrypt(username)
        description = Helper().Encrypt(description)
        suspicious = Helper().Encrypt(suspicious)
        now = datetime.datetime.now().strftime("%a %w %b %Y")


        self.cursor.execute(
            f"INSERT INTO logging (username,datetime,description,suspicious)VALUES (:user, :date,:desc,:sus)",
            {"user": username, "date": now, "desc": description, "sus": suspicious})
        self.commit()

    def get(self, table, columns, limit=None, where=1):

        query = "SELECT ? from ? WHERE ?"
        query2 = f"SELECT * from {table} WHERE ?"
        args = (columns, table, where)
        self.cursor.execute(query2, (where,))

        rows = self.cursor.fetchall()
        return rows[len(rows) - limit if limit else 0:]

    def getLast(self, table, columns):

        return self.get(table, columns, limit=1)[0]

    def createEmployee(self, kind, firstname, lastname, username, password):
        self.cursor.execute(f"INSERT INTO {kind} VALUES (:id, :first,:last,:user,:pass)",
                            {"id": None, "first": firstname, "last": lastname, "user": username,
                             "pass": password})
        self.commit()

    def createMember(self, member: Member):
        self.cursor.execute(
            f"INSERT INTO member (firstname,lastname,streetname,housenumber,zipcode,city,emailaddress,mobilephone, "
            f"date,uuid)VALUES (:first, :last,:street,:house,:zip,:city,:email,:mobile,:date,:uuid)",
            {"first": member.firstname, "last": member.lastname, "street": member.street, "house": member.housenumber,
             "zip": member.zipcode, "city": member.city, "email": member.mail, "mobile": member.mobile_number,
             "date": member.registration_date, "uuid": member.uuid})

        self.commit()



    def deletePerson(self, table, firstname, lastname):

        query = f"DELETE FROM {table} WHERE firstname = ? AND lastname = ? ;"


        args = (firstname, lastname)
        self.cursor.execute(query, args)

    def updatePassword(self, kind, password, username):

        query = f"UPDATE {kind} SET password = ? WHERE username = ?;"
        args = (password, username)
        self.cursor.execute(query, args)


    def query(self, sql, values=None):
        if values is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, values)

    def checkMigrations(self):

        try:
            self.query(
                "CREATE TABLE 'systemadmin' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT "
                "NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) "
                "NOT NULL)")
        except:
            pass
        try:
            self.query(
                "CREATE TABLE 'advisor' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, "
                "'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT "
                "NULL)")
        except:
            pass
        try:
            self.query(
                "CREATE TABLE 'member' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, "
                "'lastname' VARCHAR(128) NOT NULL, 'streetname' VARCHAR(128) NOT NULL, 'housenumber' INTEGER NOT "
                "NULL, 'zipcode' VARCHAR(128) NOT NULL, 'city' VARCHAR(128) NOT NULL, 'emailaddress' VARCHAR(128) NOT "
                "NULL, 'mobilephone' VARCHAR(128) NOT NULL, 'date' VARCHAR(128) NOT NULL,'uuid' VARCHAR(128) NOT NULL)")
        except:
            pass
        try:
            self.query(
                "CREATE TABLE 'superadmin' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT "
                "NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) "
                "NOT NULL)")
        except:
            pass
        try:
            self.query(
                "CREATE TABLE 'logging' ('number' INTEGER PRIMARY KEY AUTOINCREMENT, 'username' VARCHAR(128) NOT "
                "NULL, 'datetime' VARCHAR(128) NOT NULL, 'description' VARCHAR(128) NOT NULL, 'suspicious' VARCHAR("
                "128) NOT NULL)")
        except:
            pass
        self.open("analyse.db")
        self.commit()
