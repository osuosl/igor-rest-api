from api import app
from flask import session, url_for, g
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.httpauth import HTTPBasicAuth
from models import db, User, Machine

# Define the HTTP error codes we use
CREATED = 201 
BAD_REQUEST = 400 
UNAUTHORIZED = 401 
NOT_FOUND = 404 
FORBIDDEN = 403 

# Constants
TOKEN_EXPIRATION = 600 # 10 minutes

igor_api = Api(app)

# Authentication
auth = HTTPBasicAuth()

@auth.verify_password
def validate_password(username_or_token, password):
    user = User.validate_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True

"""
    GET     /login            Generates an returns an authentication token
"""
class LoginAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        token = g.user.generate_auth_token(TOKEN_EXPIRATION)
        return {'token': token.decode('ascii'), 'duration': TOKEN_EXPIRATION}

igor_api.add_resource(LoginAPI, '/login', endpoint='login')

# User management endpoints
"""
    GET     /users                           Returns the list of users
    POST    /users {'username': username,
                    'password': password}    Creates a new user
"""
class UsersAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(UsersAPI, self).__init__()

    def get(self):
        users = []
        for user in User.query.all():
            users.append(user.username)
        return {'users': [{'username': username,
                           'location': url_for('user', username=username, _external=True)}
                          for username in users]}

    def post(self):
        args = self.reqparse.parse_args()
        
        username = args['username']
        password = args['password']
        if User.query.filter_by(username=username).first() is not None:
            return {'message': 'User %s exists' % username}, BAD_REQUEST 
        else:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            return {'username': user.username,
                    'location': url_for('user', username=user.username, _external=True)}, CREATED
        
"""
    GET     /users/:username             Returns details for user <username>
    DELETE  /users/:username             Deletes user <username>
    PUT     /users/:username             Updates password for user <username>
"""
class UserAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(UserAPI, self).__init__()

    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            return {'username': user.username,
                    'location': url_for('user', username=username, _external=True)}

    def delete(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot delete user %s' % (g.user.username, username)}

        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User %s deleted' % user.username}

    def put(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot modify user %s' % (g.user.username, username)}
        
        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=username).first()
        password = args['password']
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'Updated entry for user %s' % username}

igor_api.add_resource(UsersAPI, '/users', endpoint='users')
igor_api.add_resource(UserAPI, '/users/<string:username>', endpoint='user')

# Machine management endpoints
"""
    GET     /machines                           Returns the list of machines
    POST    /machines {'hostname': hostname,
                       'username': username,
                       'fqdn':     FQDN,
                       'password': password}    Creates a new machine entry
"""
class MachinesAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hostname', type=str, required=True,
                                    help='No hostname provided', location='json')
        self.reqparse.add_argument('fqdn', type=str, required=True,
                                    help='No FQDN provided', location='json')
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(MachinesAPI, self).__init__()

    def get(self):
        machines = []
        for machine in Machine.query.all():
            machines.append(machine.hostname)
        return {'machines': [{'hostname': hostname,
                              'location': url_for('machine', hostname=hostname, _external=True)}
                              for hostname in machines]}

    def post(self):
        args = self.reqparse.parse_args()

        hostname = args['hostname']
        fqdn = args['fqdn']
        username = args['username']
        password = args['password']
        if Machine.query.filter_by(hostname=hostname).first() is not None:
            return {'message': 'Host %s exists' % hostname}, BAD_REQUEST
        else:
            machine = Machine(hostname, fqdn, username, password)
            db.session.add(machine)
            db.session.commit()
            return {'hostname': machine.hostname,
                    'location': url_for('machine', hostname=machine.hostname, _external=True)}, CREATED

"""
    GET     /machines/:hostname             Returns details for machine <hostname>
    DELETE  /machines/:hostname             Deletes machine <hostname>
    PUT     /machines/:hostname             Updates FQDN, username and password for machine <hostname>
"""
class MachineAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('fqdn', type=str, required=True,
                                    help='No FQDN provided', location='json')
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(MachineAPI, self).__init__()

    def get(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not hostname:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            return {'hostname': machine.hostname,
                    'fqdn': machine.fqdn,
                    'location': url_for('machine', hostname=hostname, _external=True)}

    def delete(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            db.session.delete(machine)
            db.session.commit()
            return {'message': 'Host %s deleted' % machine.hostname}

    def put(self, hostname):
        args = self.reqparse.parse_args()
        machine = Machine.query.filter_by(hostname=hostname).first()
        fqdn = args['fqdn']
        username = args['username']
        password = args['password']
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            machine.fqdn = fqdn
            machine.username = username
            machine.password = password
            db.session.add(machine)
            db.session.commit()
            return {'message': 'Updated entry for host %s' % hostname}

igor_api.add_resource(MachinesAPI, '/machines', endpoint='machines')
igor_api.add_resource(MachineAPI, '/machines/<string:hostname>', endpoint='machine')
