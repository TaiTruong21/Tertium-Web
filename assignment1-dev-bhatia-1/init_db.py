# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

#######################
# CONNECT TO DATABASE #
#######################
print('--> CONNECTING TO DATABASE')
db_user = os.environ['MYSQL_USER']
db_user = "root"
db_pass = os.environ['MYSQL_PASSWORD']
db_pass = os.environ['MYSQL_ROOT_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = 'localhost' # different than inside the container and assumes default port of 3306

db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass, use_pure=True, port=3307)
cursor = db.cursor()

###################
# CLEARING TABLES #
###################
cursor.execute("drop table if exists TUsers;")

#################
# CREATE TABLES #
#################
print('--> CREATING TABLES')
try:
    print('   --> CREATING TUsers')
    querry = """CREATE TABLE TUsers (
                id integer  AUTO_INCREMENT PRIMARY KEY,
                firstname   VARCHAR(30) NOT NULL,
                lastname   VARCHAR(30) NOT NULL,
                email       VARCHAR(30) NOT NULL
                );"""
    cursor.execute(querry)
except Exception:
    print("ERROR Making Table")

#############################
# DONE INITLAIZING DATABASE #
#############################
db.close()
print('--> DATABASE INITIALIZED')
