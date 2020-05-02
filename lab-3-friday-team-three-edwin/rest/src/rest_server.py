from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import json

import mysql.connector as mysql
import os

import time
import datetime

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']


def set_Status(req):
    """
    with open('database.json', 'r') as db_file:
        users = json.load(db_file)['users']
    counter = 0
    for user in users:
        if(user['userId'] == req.POST['userId']):
            users[counter]['status'] = req.POST['changeStatus']
        counter = counter+1
    user_list = {'users': users}
    with open('database.json', 'w') as db_file:
        json.dump(user_list, db_file, indent=4)
    with open('database.json', 'r') as db_file:
        users = json.load(db_file)
    """
    db = mysql.connect(host=db_host, database=db_name,
                       user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("UPDATE Users SET status='%s' WHERE username='%s';" %
                   (req.POST['changeStatus'], req.POST['userId']))
    db.commit()
    records = cursor.fetchall()
    db.close()
    response = []
    for record in records:
        response.append({
            'userId':   record[0],
            'password': record[1],
            'status':   record[2]
        })
    return response


def get_users(req):
    """
    # Read form local json
    with open('database.json', 'r') as db_file:
        users = json.load(db_file)['users']
    """

    db = mysql.connect(host=db_host, database=db_name,
                       user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT username, password, status FROM Users;")
    records = cursor.fetchall()
    db.close()
    print(records)
    response = []
    for record in records:
        response.append({
            'userId':   record[0],
            'password': record[1],
            'status':   record[2]
        })
    print(json.dumps(response))
    return response


def add_user(req):
    """
    print("add_user: " + req.POST['userId'])
    newUser = {"userId": req.POST['userId'],
               "password": req.POST['password'], "status": "Pending"}
    with open('database.json', 'r') as db_file:
        prev_users = json.load(db_file)
        updated_users = prev_users['users']
        updated_users.append(newUser)
        user_list = {'users': updated_users}
    with open('database.json', 'w') as db_file:
        json.dump(user_list, db_file, indent=4)
    with open('database.json', 'r') as db_file:
        users = json.load(db_file)
    """

    db = mysql.connect(host=db_host, database=db_name,
                       user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("INSERT INTO Users (username, password, status) VALUE ('%s', '%s', 'Pending');" % (
        req.POST['userId'], req.POST['password']))
    db.commit()
    cursor.execute("SELECT username, password, status FROM Users;")
    records = cursor.fetchall()
    db.close()
    response = []
    for record in records:
        response.append({
            'userId':   record[0],
            'password': record[1],
            'status':   record[2]
        })
    print(json.dumps(response))
    return response


def post_handler(req):
    if 'changeStatus' in req.POST:
        return set_Status(req)
    else:
        return add_user(req)


def get_pending_moves(req):
    db = mysql.connect(host=db_host, database=db_name,
                       user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Moves where status='pending';")
    records = cursor.fetchall()
    db.close()
    response = []
    for record in records:
        response.append({
            'moveId':       record[0],
            'initiateTime': str(record[1]),
            'startTime':    str(record[2]),
            'endTime':      str(record[3]),
            'direction':    record[4],
            'userId':       record[5],
            'status':       record[6],
        })
    return response


def get_complete_moves(req):
    db = mysql.connect(host=db_host, database=db_name,
                       user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Moves where status='complete';")
    records = cursor.fetchall()
    db.close()
    response = []
    for record in records:
        response.append({
            'moveId':       record[0],
            'initiateTime': str(record[1]),
            'startTime':    str(record[2]),
            'endTime':      str(record[3]),
            'direction':    record[4],
            'userId':       record[5],
            'status':       record[6],
        })
    return response


def get_moves(req):
    db = mysql.connect(host=db_host, database=db_name,
                       user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Moves;")
    records = cursor.fetchall()
    db.close()
    response = []
    for record in records:
        response.append({
            'moveId':       record[0],
            'initiateTime': str(record[1]),
            'startTime':    str(record[2]),
            'endTime':      str(record[3]),
            'direction':    record[4],
            'userId':       record[5],
            'status':       record[6],
        })
    return response


def fetch_move(req):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    try:
        db = mysql.connect(host=db_host, database=db_name,
                        user=db_user, passwd=db_pass)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Moves where status='pending' LIMIT 1;")
        record = cursor.fetchone()
        cursor.execute("UPDATE Moves SET startTime='%s',status='inprogress' where moveId=%s" %(timestamp, record[0]))
        db.commit()
        db.close()
        print(record)
        response = {
                'moveId':       record[0],
                'initiateTime': str(record[1]),
                'startTime':    str(record[2]),
                'endTime':      str(record[3]),
                'direction':    record[4],
                'userId':       record[5],
                'status':       record[6],
            }
        return response
    except:
        return "Null"

def finish_move(req):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    moveId = req.matchdict['mid']
    db = mysql.connect(host=db_host, database=db_name,
                       user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("UPDATE Moves SET status='complete' where moveId=%s;" %moveId)
    cursor.execute("UPDATE Moves SET endTime='%s' where moveId=%s" %(timestamp, moveId))
    db.commit()
    db.close()
    return

def push_move(req):
    direction = req.matchdict['dir']
    uid = req.matchdict['uid']
    db = mysql.connect(host=db_host, database=db_name,
                       user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("INSERT INTO Moves (direction, userId, status) VALUE('%s', '%s', 'pending')" %(direction, uid))
    db.commit()
    db.close()
    return

if __name__ == '__main__':
    config = Configurator()

    config.add_route('rest_route', '/users')
    config.add_view(get_users, route_name='rest_route', renderer='json')
    config.add_view(post_handler, route_name='rest_route',
                    renderer='json', request_method='POST')

    config.add_route('moves_pending_route', '/moves/pending')
    config.add_view(get_pending_moves,
                    route_name='moves_pending_route', renderer='json')
    config.add_route('moves_complete_route', '/moves/complete')
    config.add_view(get_complete_moves,
                    route_name='moves_complete_route', renderer='json')

    config.add_route('moves_route', '/moves')
    config.add_view(get_moves,
                    route_name='moves_route', renderer='json')

    config.add_route('moves_next_route', '/moves/next')
    config.add_view(fetch_move,
                    route_name='moves_next_route', renderer='json')
    config.add_route('moves_finish_route', 'moves/fin/{mid}')
    config.add_view(finish_move, route_name='moves_finish_route', renderer='json')

    config.add_route('push_move_route', 'moves/add/{dir}/{uid}')
    config.add_view(push_move, route_name='push_move_route', renderer='json')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
