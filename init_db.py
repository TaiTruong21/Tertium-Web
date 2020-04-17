# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = 'localhost' # different than inside the container and assumes default port of 3306

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# Create a Printers table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE Printers (
      id integer  AUTO_INCREMENT PRIMARY KEY,
      first_name  VARCHAR(30) NOT NULL,
      last_name   VARCHAR(30) NOT NULL,
      email       VARCHAR(50) NOT NULL,
      created_at  TIMESTAMP
    );
  """)
except:
  print("Table already exists. Not recreating it.")

# Create a Customers table (wrapping it in a try-except is good practice)
try:
  cursor.execute("""
    CREATE TABLE Customers (
      id integer  AUTO_INCREMENT PRIMARY KEY,
      first_name  VARCHAR(30) NOT NULL,
      last_name   VARCHAR(30) NOT NULL,
      email       VARCHAR(50) NOT NULL,
      created_at  TIMESTAMP
    );
  """)
except:
  print("Table already exists. Not recreating it.")

# Selecting Records
cursor.execute("select * from TUsers;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

db.close()
