from flask import g
from flask.ext.restful import Resource

from igor_rest_api.api.constants import *
from igor_rest_api.api.auth.login import auth

# Login endpoint
"""
    GET     /login            Generates an returns an authentication token
"""
class LoginAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        token = g.user.generate_auth_token(TOKEN_EXPIRATION)
        return {'token': token.decode('ascii'), 'duration': TOKEN_EXPIRATION}
