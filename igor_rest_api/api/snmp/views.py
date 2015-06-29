#!/usr/bin/env python

from flask import g, url_for
from flask.ext.restful import Resource, reqparse

from igor_rest_api.api.constants import *
from igor_rest_api.db import db

from .login import auth
from .models import Snmpuser


# User management endpoints
"""
    GET     /snmpusers                           Returns the list of users
    POST    /snmpusers {'username': username,
                    'password': password}    Creates a new user
"""


class SNMPUsersAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='No username provided',
                                   location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='No password provided',
                                   location='json')
        super(SNMPUsersAPI, self).__init__()

    def get(self):
        users = []
        for user in Snmpuser.query.all():
            users.append(user.username)
        return {'users': [{'username': username,
                           'location': url_for('snmpuser', username=username,
                                               _external=True)}
                          for username in users]}

    def post(self):
        args = self.reqparse.parse_args()

        if g.user.username != 'root':
            return {'Error': 'only root can add users'}

        username = args['username']
        password = args['password']
        if Snmpuser.query.filter_by(username=username).first() is not None:
            return {'message': 'User %s exists' % username}, BAD_REQUEST
        else:
            user = Snmpuser(username, password)
            db.session.add(user)
            db.session.commit()
            return {'username': user.username,
                    'pdus': url_for('user_pdus',
                                    username=username, _external=True),
                    'location': url_for('snmpuser',
                                        username=user.username,
                                        _external=True)}, CREATED

"""
    GET     /snmpusers/:username           Returns details for user <username>
    DELETE  /snmpusers/:username           Deletes user <username>
    PUT     /snmpusers/:username           Updates password for user <username>
"""


class SNMPUserAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='No password provided',
                                   location='json')
        super(SNMPUserAPI, self).__init__()

    def get(self, username):
        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            return {'username': user.username,
                    'pdus': url_for('user_pdus',
                                    username=username, _external=True),
                    'location': url_for('snmpuser',
                                        username=username, _external=True)}

    def delete(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot delete user %s' %
                    (g.user.username, username)}, BAD_REQUEST

        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User %s deleted' % user.username}

    def put(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot modify user %s' %
                    (g.user.username, username)}

        args = self.reqparse.parse_args()
        user = Snmpuser.query.filter_by(username=username).first()
        password = args['password']
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'Updated entry for user %s' % username}


# Login endpoint
"""
    GET     /snmplogin            Generates an returns an authentication token
"""


class SNMPLoginAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        token = g.user.generate_auth_token(TOKEN_EXPIRATION)
        return {'token': token.decode('ascii'), 'duration': TOKEN_EXPIRATION}
