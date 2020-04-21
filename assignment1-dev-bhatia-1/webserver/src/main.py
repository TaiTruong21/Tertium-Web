import os
import sys
import time
import json
import datetime
from dotenv import load_dotenv
import mysql.connector as mysql
from pyramid.response import Response
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from pyramid.renderers import render_to_response

load_dotenv('credentials.env')

def execute_querry(querry):
    db_user = os.environ['MYSQL_USER']
    db_pass = os.environ['MYSQL_PASSWORD']
    db_name = os.environ['MYSQL_DATABASE']
    db_host = "tertiumA1" # different than inside the container and assumes default port of 3306
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass, use_pure=True, port=3306)
    cursor = db.cursor()
    cursor.execute(querry)

def show_landing_page(req):
    return render_to_response("html/landing.html", {}, request=req)

def show_about_page(req):
    return render_to_response("html/about.html", {}, request=req)

def show_team_page(req):
    return render_to_response("html/team.html", {}, request=req)

def show_email_page(req):
    return render_to_response("html/email.html", {}, request=req)

def get_post_signup(req):
    first = req.POST['first']
    last = req.POST['last']
    email = req.POST['email']
    querry = """INSERT INTO TUsers (firstname, lastname, email) VALUES ('{}', '{}', '{}');""".format(first, last, email)
    execute_querry(querry)
    return render_to_response("html/thanks.html", {}, request=req)

"""Route Configurations"""
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route("landing", "/")
  config.add_view(show_landing_page, route_name="landing")

  config.add_route("team", "/team")
  config.add_view(show_team_page, route_name="team")

  config.add_route("about", "/about")
  config.add_view(show_about_page, route_name="about")

  config.add_route("signup", "/signup")
  config.add_view(show_email_page, route_name="signup")

  config.add_route("post_signup", "/thanks")
  config.add_view(get_post_signup, route_name="post_signup", request_method="POST")

  config.add_static_view(name='/', path='./public', cache_max_age=3600) #expose the public folder for the CSS file
  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()
