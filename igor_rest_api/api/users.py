#!/usr/bin/env python

from flask import g, url_for
from flask.ext.restful import Resource, reqparse

from .constants import *
from .models import db, User
from .login import auth

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
                                    help='No username provided',
                                    location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided',
                                    location='json')
        super(UsersAPI, self).__init__()

    def get(self):
        users = []
        for user in User.query.all():
            users.append(user.username)
        return {'users': [{'username': username,
                           'location': url_for('user', username=username,
                                               _external=True)}
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
                    'machines': url_for('user_machines', username=username,
                                         _external=True),
                    'location': url_for('user', username=user.username,
                                        _external=True)}, CREATED

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
                    'machines': url_for('user_machines', username=username, _external=True),
                    'location': url_for('user', username=username, _external=True)}

    def delete(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot delete user %s' % (g.user.username, username)},\
                   BAD_REQUEST

        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            user.machines = []
            db.session.add(user)
            db.session.commit()
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
