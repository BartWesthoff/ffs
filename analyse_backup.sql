BEGIN TRANSACTION;
CREATE TABLE 'Logging' ('number' INTEGER PRIMARY KEY AUTOINCREMENT, 'username' VARCHAR(128) NOT NULL, 'datetime' VARCHAR(128) NOT NULL, 'description' VARCHAR(128) NOT NULL, 'suspicious' VARCHAR(128) NOT NULL);
CREATE TABLE 'advisor' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT NULL);
CREATE TABLE 'member' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, 'lastname' VARCHAR(128) NOT NULL, 'streetname' VARCHAR(128) NOT NULL, 'housenumber' INTEGER NOT NULL, 'zipcode' VARCHAR(128) NOT NULL, 'city' VARCHAR(128) NOT NULL, 'emailaddress' VARCHAR(128) NOT NULL, 'mobilephone' VARCHAR(128) NOT NULL, 'date' VARCHAR(128) NOT NULL);
INSERT INTO "member" VALUES(4,'Rmipw','Ovs','oeew',55,'5678EE','Vsxxivheq','a@lv.rp','75-0-56789012','2022-06-19 19:25:12.457446');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('advisor',1);
INSERT INTO "sqlite_sequence" VALUES('member',4);
INSERT INTO "sqlite_sequence" VALUES('systemadmin',1);
CREATE TABLE 'superadmin' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT NULL);
CREATE TABLE 'systemadmin' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'firstname' VARCHAR(128) NOT NULL, 'lastname' VARCHAR(128) NOT NULL, 'username' VARCHAR(128) NOT NULL, 'password' VARCHAR(128) NOT NULL);
INSERT INTO "systemadmin" VALUES(1,'Rmipw','Ovsqqirlsio','ywivreqi','Ehqmr567!');
COMMIT;
