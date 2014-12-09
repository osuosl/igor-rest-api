import sqlalchemy

from flask import g, url_for
from flask.ext.restful import Resource, reqparse, fields, marshal_with

from igor_rest_api.api.exceptions import (
    NotAuthorized, ResourceDoesNotExist, UserAlreadyExists
)
from igor_rest_api.api.auth.login import auth
from igor_rest_api.api.auth.models import User
from igor_rest_api.api.constants import *
from igor_rest_api.api.models import db

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

machine_fields = {
    'machines': fields.List(fields.Nested({
        "id": fields.Integer,
        "hostname": fields.String,
    }))
}

user_fields_with_machines = user_fields.copy()
user_fields_with_machines.update(machine_fields)

class UsersAPI(Resource):
    decorators = [auth.login_required]

    # This can go away when 0.3.1 is released with the
    # envelope keyword arg in marshal_with(user_fields, envelop="users")
    users_fields = {
        "users": fields.Nested(user_fields)
    }

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided',
                                    location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided',
                                    location='json')
        super(UsersAPI, self).__init__()

    @marshal_with(users_fields)
    def get(self, **kwargs):
        """
        Returns a list of users under the key "users"
        """
        return {"users": User.query.all()}

    @marshal_with(user_fields)
    def post(self):
        """
        Accepts a JSON object containing username and password keys. Returns
        the user object.
        """
        args = self.reqparse.parse_args()

        username = args['username']
        password = args['password']
        try:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            raise UserAlreadyExists(username)
        return user


class UserAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(UserAPI, self).__init__()

    @marshal_with(user_fields_with_machines)
    def get(self, username):
        """
        Returns a user with the id, username and machines fields
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ResourceDoesNotExist("User %s does not exist!" % username)
        return user

    @marshal_with(user_fields)
    def delete(self, username):
        """
        Deletes a user and returns the id and username if sucessful
        """
        if g.user.username != 'root' and g.user.username != username:
            raise NotAuthorized(g.user.username)

        user = User.query.filter_by(username=username).first()
        if not user:
            raise ResourceDoesNotExist("User %s does not exist!" % username)
        else:
            db.session.delete(user)
            db.session.commit()
            return user

    @marshal_with(user_fields)
    def put(self, username):
        """
        Updates a user's password and returns the id and username if sucessful
        """
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot modify user %s' % (g.user.username, username)}

        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=username).first()
        password = args['password']
        if not user:
            raise ResourceDoesNotExist("User %s does not exist!" % username)
        else:
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user


class UserMachinesAPI(Resource):
    decorators = [auth.login_required]

    @marshal_with(machine_fields)
    def get(self, username):
        """
        Returns the list of machines accessible by the given username
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ResourceDoesNotExist("User %s does not exist!" % username)
        return {'machines': user.machines}

