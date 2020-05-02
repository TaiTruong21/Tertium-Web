from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.security import Allow, Authenticated, remember, forget, authenticated_userid
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

import requests
import os

REST_SERVER = os.environ['REST_SERVER']


def get_admin(req):
    users = requests.get(REST_SERVER + "/users").json()
    return render_to_response('templates/admin.html', {'users': users}, request=req)


def update_admin(req):
    users = requests.get(REST_SERVER + "/users").json()
    if 'void' in req.POST:
        print("void " + req.POST['void'])
        requests.post(REST_SERVER + "/users",
                      {"userId": req.POST['void'], "changeStatus": "Voided"})
    if 'verify' in req.POST:
        print("verify " + req.POST['verify'])
        requests.post(REST_SERVER + "/users",
                      {"userId": req.POST['verify'], "changeStatus": "Verified"})
    users = requests.get(REST_SERVER + "/users").json()
    return render_to_response('templates/admin.html', {'users': users}, request=req)


def signUp(req):
    if((not req.POST['email'].isalnum()) or (not req.POST['password'].isalnum())):
        return False

    users = requests.get(REST_SERVER + "/users").json()
    for user in users:
        if(user['userId'] == req.POST['email']):
            return False
    requests.post(REST_SERVER + "/users",
                  {"userId": req.POST['email'], "password": req.POST['password'], "status": "Pending"})
    return True


def get_signup(req):
    return render_to_response('templates/show_signup.html', {}, request=req)


def post_signup(req):
    if(signUp(req)):
        return render_to_response('templates/did_signup.html', {}, request=req)
    else:
        return render_to_response('templates/show_signup.html', {'error': 'The user already exists'}, request=req)

# --- this is called to compare credentials to the value


def is_valid_user(req):
    users = requests.get(REST_SERVER + "/users").json()
    print("Login attempted by: " +
          req.POST['email'] + ", password: " + req.POST['password'])
    for user in users:
        if(user['userId'] == req.POST['email']):
            if(user['password'] == req.POST['password']):
                if(user['status'] == "Verified"):
                    return True
                else:
                    return False
            else:
                return False
    return False

# --- this route will validate login credentials...


def post_login(req):
    if is_valid_user(req):
        headers = remember(req, req.POST['email'])
        response = req.response
        response.headerlist.extend(headers)
        return render_to_response('templates/did_login.html', {'username': req.POST['email']}, request=req, response=response)
    else:
        return render_to_response('templates/show_login.html', {'error': 'invalid credentials'}, request=req)


# --- this route will show a login form


def get_login(req):
    return render_to_response('templates/show_login.html', {}, request=req)


# --- this route will show the logout page


def get_logout(req):
    headers = forget(req)
    response = req.response
    response.headerlist.extend(headers)
    return render_to_response('templates/get_logout.html', {}, request=req, response=response)


def get_controller(req):
    # TODO Implement logic to update data to rest_server
    return render_to_response('templates/jetbot_controller.html', {'UserId': req.matchdict['UserId']}, request=req)


def post_move(req):
    requests.get(REST_SERVER + "/moves/add/" +
                 req.matchdict['Dir'] + "/" + req.matchdict['UserId'])
    return render_to_response('templates/jetbot_controller.html', {'UserId': req.matchdict['UserId']}, request=req)


def get_tracker(req):
    moves = requests.get(REST_SERVER + "/moves").json()
    return render_to_response('templates/jetbot_tracker.html', {'moves': moves}, request=req)


def get_portal(req):
    return render_to_response('templates/portal.html', {'UserId': req.matchdict['UserId']}, request=req)


class RootFactory(object):
    def __init__(self, req):
        self.__acl__ = [(Allow, Authenticated, 'authenticated')]


if __name__ == '__main__':
    authn_policy = AuthTktAuthenticationPolicy('soseekrit')
    authr_policy = ACLAuthorizationPolicy()
    config = Configurator(
        root_factory=RootFactory,
        authentication_policy=authn_policy,
        authorization_policy=authr_policy
    )

    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    config.add_route('login', '/login')
    config.add_view(get_login, route_name='login')
    config.add_view(post_login, route_name='login', request_method='POST')

    config.add_route('logout', '/logout')
    config.add_view(get_logout, route_name='logout')

    config.add_route('signup', '/signup')
    config.add_view(get_signup, route_name='signup')
    config.add_view(post_signup, route_name='signup', request_method='POST')

    config.add_route('admin', '/admin')
    config.add_view(get_admin, route_name='admin', permission='authenticated')
    config.add_view(update_admin, route_name='admin',
                    request_method='POST', permission='authenticated')

    config.add_route('controller', '/controller/{UserId}')
    config.add_view(get_controller, route_name='controller',
                    permission='authenticated')

    config.add_route('controller_move', '/controller/{UserId}/{Dir}')
    config.add_view(post_move, route_name='controller_move',
                    request_method="POST", permission='authenticated')

    config.add_route('tracker', '/tracker')
    config.add_view(get_tracker, route_name='tracker',
                    permission='authenticated')

    config.add_route('portal', '/portal/{UserId}')
    config.add_view(get_portal, route_name='portal',
                    permission='authenticated')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
