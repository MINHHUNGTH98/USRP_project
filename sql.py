#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect(host = "localhost",user = "root", passwd = "1",db ="usrp")

# prepare a cursor object using cursor() method
# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = """CREATE TABLE USRP (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

db.close()