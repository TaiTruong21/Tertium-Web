from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from pyramid.renderers import render_to_response

import json
import mysql.connector as mysql
import os
import requests
import collections
import time

UI_SERVER = os.environ['UI_SERVER']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def post_SignupUser(req):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()

    data = req.json_body
    query = "INSERT into Users (email, name, password) values (%s, %s, %s)" 
    email = data['email']
    name = data['name']
    password = data['password']
    values = [(email,name,password)]
    print(values)
    cursor.executemany(query, values)
    db.commit() #Committing the signup credentials to the database

    #Displaying the updated table:
    cursor.execute("""Select * from Users;""")
    records = cursor.fetchall()
    print('Updated Users table:')
    print(records)
    db.close()
    return None

def post_SignupPrinter(req):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()

    data = req.json_body
    query = "INSERT into Printers (email,name,password, printer, address) values (%s, %s, %s, %s, %s)" 
    email = data['email']
    name = data['name']
    password = data['password']
    printer = data['printer']
    address = data['address']
    values = [(email,name,password, printer, address)]
    print(values)
    cursor.executemany(query, values)
    db.commit() #Committing the signup credentials to the database

    #Displaying the updated table:
    cursor.execute(
    """Select * from Printers;""")
    records = cursor.fetchall()
    print('Updated Printers table:')
    print(records)
    db.close()
    return None

''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.add_route('post_SignupUser', '/User')
  config.add_view(post_SignupUser, route_name='post_SignupUser', renderer='json', request_method ='POST')

  config.add_route('post_SignupPrinter', '/Printer')
  config.add_view(post_SignupPrinter, route_name='post_SignupPrinter', renderer='json', request_method ='POST')

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()
  
