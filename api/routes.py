from api import app
from flask import session, url_for, g
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.httpauth import HTTPBasicAuth
from models import db, User

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
    GET     /user                           Returns the list of users
    POST    /user {'username': username,
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
    GET     /user/:username             Returns details for user <username>
    DELETE  /user/:username             Deletes user <username>
    PUT     /user/:username :password   Updates password for user <username>
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
