  
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response

import json
import requests
import os
import time
REST_SERVER = os.environ['REST_SERVER']

############################## Website rendering #########################
def main_page(req):
    return render_to_response('homepage.html',{}, request=req)

def get_SignupUser(req):
    return render_to_response('SignupUser.html',{}, request=req)

def get_SignupPrinter(req):
    return render_to_response('SignupPrinter.html',{}, request=req)

def get_AboutUs(req):
    return render_to_response('AboutUs.html',{}, request=req)

############################## Users Info #################################
def post_SignupUser(req):
    user_data={
        'email': req.params['email'],
        'name': req.params['name'],
        'password': req.params['password']
    }
    requests.post(REST_SERVER + "/User", json=user_data)
    return render_to_response('homepage.html',{}, request=req)
def post_SignupPrinter(req):
    printer_data={
        'email': req.params['email'],
        'name': req.params['name'],
        'password': req.params['password'],
        'printer': req.params['printer'],
        'address': req.params['address']
    }
    requests.post(REST_SERVER + "/Printer", json=printer_data)
    return render_to_response('homepage.html',{}, request=req)

############################## Configuration ##############################
if __name__ == '__main__':
#  config = Configurator()
    with Configurator() as config:

        config.include('pyramid_jinja2')
        config.add_jinja2_renderer('.html')

        config.add_route('homepage', '/')
        config.add_view(main_page, route_name='homepage', request_method='GET')

        config.add_route('SignupUser','/SignupUser')
        config.add_view(get_SignupUser, route_name='SignupUser', request_method='GET')
        config.add_view(post_SignupUser, route_name='SignupUser', request_method='POST')

        config.add_route('SignupPrinter','/SignupPrinter')
        config.add_view(get_SignupPrinter, route_name='SignupPrinter', request_method='GET')
        config.add_view(post_SignupPrinter, route_name='SignupPrinter', request_method='POST')

        config.add_route('AboutUs','/AboutUs')
        config.add_view(get_AboutUs, route_name='AboutUs', request_method='GET')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()

server = make_server('0.0.0.0', 5000, app)
server.serve_forever()



