import mysql.connector as mysql
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = 'localhost' 

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# Clean up past data
cursor.execute("drop table if exists Users;")
cursor.execute("drop table if exists Printers;")

# creating table schemas
try:
  cursor.execute("""
    CREATE TABLE Users(
        id integer  AUTO_INCREMENT PRIMARY KEY,
        email    VARCHAR(50) NOT NULL,
        name    VARCHAR(50) NOT NULL,
        password      VARCHAR(50) NOT NULL
    );
  """)
except:
  print("Table Users already exists. Not recreating it.")

try:
  cursor.execute("""
    CREATE TABLE Printers(
        id integer  AUTO_INCREMENT PRIMARY KEY,
        email    VARCHAR(50) NOT NULL,
        name    VARCHAR(50) NOT NULL,
        password      VARCHAR(50) NOT NULL,
        printer VARCHAR(50) NOT NULL,
        address VARCHAR(100) NOT NULL
    );
  """)
except:
  print("Table Printers already exists. Not recreating it.")

db.commit()
# Tables
print('---------- TABLES ----------')
[print(x) for x in cursor]
print('\n\n')
cursor.execute("describe Users;")
[print(x) for x in cursor]
print('\n\n')
cursor.execute("describe Printers;")
[print(x) for x in cursor]
print('\n\n')

db.close()
