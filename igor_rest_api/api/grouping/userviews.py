#!/usr/bin/env python

from flask import g, url_for
from flask.ext.restful import Resource, reqparse

from igor_rest_api.api.constants import *
from igor_rest_api.db import db

from .login import rootauth, auth
from .models import Userdetails, Useroutletsgroups

# User management endpoints
"""
    GET     /outlet_groups/users                           Returns the list of users
    POST    /outlet_groups/users {'username': username,
                    'password': password}    Creates a new user
"""
class GroupingusersAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided',
                                    location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided',
                                    location='json')
        super(GroupingusersAPI, self).__init__()

    def get(self):
        users = []
        for user in Userdetails.query.all():
            users.append(user.username)
        return {'users': [{'username': username,
                           'location': url_for('groupingsuser', username=username,
                                               _external=True)}
                          for username in users]}

    def post(self):
        args = self.reqparse.parse_args()

        if g.user.username != 'root':
            return {'message': 'only root can add users'}
        username = args['username']
        password = args['password']
        if Userdetails.query.filter_by(username=username).first() is not None:
            return {'message': 'User %s exists' % username}, BAD_REQUEST
        else:
            user = Userdetails(username, password)
            db.session.add(user)
            db.session.commit()
            return {'username': user.username,
                    #'groupings': url_for('user_groupings', username=username,
                    #                     _external=True),
                    'location': url_for('groupingsuser', username=user.username,
                                        _external=True)}, CREATED

"""
    GET     /outlet_groups/users/:username             Returns details for user <username>
    DELETE  /outlet_groups/users/:username             Deletes user <username>
    PUT     /outlet_groups/users/:username             Updates password for user <username>
"""
class GroupinguserAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided', location='json')
        super(GroupinguserAPI, self).__init__()

    def get(self, username):
        user = Userdetails.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            return {'username': user.username,
                    #'outlet_groups': url_for('user_outlet_groups', username=username, _external=True),
                    'location': url_for('outlet_groupsuser', username=username, _external=True)}

    def delete(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot delete user %s' % (g.user.username, username)},\
                   BAD_REQUEST

        user = Userdetails.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            db.session.add(user)
            db.session.commit()
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User %s deleted' % user.username}

    def put(self, username):
        if g.user.username != 'root' and g.user.username != username:
            return {'message': '%s cannot modify user %s' % (g.user.username, username)}

        args = self.reqparse.parse_args()
        user = Userdetails.query.filter_by(username=username).first()
        password = args['password']
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND
        else:
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'Updated entry for user %s' % username}


"""
    GET     /outlet_groups/user/groups          Returns associations between users and outletgroupings
    POST    /outlet_groups/user/groups  {'outletgroupid': outletgroupid,
                                'userid': userid }    Creates association between user and outletgroupings
    DELETE /outlet_groups/user/groups  {'outletgroupid': outletgroupid,
                                'userid': userid }    Deletes the association between user and outletgrouping
"""
class Usergroups(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userid', type=int, required=True,
                                    help='No userid provided',
                                    location='json')
        self.reqparse.add_argument('outletgroupid', type=int, required=True,
                                    help='No outletgroupid provided',
                                    location='json')
        super(Usergroups, self).__init__()

    def get(self):
        relations = Useroutletsgroups.query.all()
        return {'relations': [{'userid': relation.userid,
                            'outletgroupid': relation.outletgroupid}
                            for relation in relations]}
    def post(self):
        args = self.reqparse.parse_args()

        if g.user.username != 'root':
            return {'message': 'only root can add users to outlet groups'}
        userid = args['userid']
        user = Userdetails.query.filter_by(id=userid).first()
        if user is None:
            return {'message' : 'User does not exist'}
        outletgroupid = args['outletgroupid']
        if Useroutletsgroups.query.filter_by(userid=userid,outletgroupid=outletgroupid).first() is not None:
            return {'message': 'Relation between Userid %s and outletgroup %s exists' % (userid, outletgroupid)}, BAD_REQUEST
        else:
            relation = Useroutletsgroups(userid, outletgroupid)
            db.session.add(relation)
            db.session.commit()
            return {'username': user.username,
                    'grouping': url_for('groupings_group', id=outletgroupid,
                                         _external=True),
                    'location': url_for('groupingsuser', username=user.username,
                                        _external=True)}, CREATED

    def delete(self):
        args = self.reqparse.parse_args()
        if g.user.username != 'root':
            return {'message' : 'only root can delete relations '}
        userid = args['userid']
        outletgroupid = args['outletgroupid']
        if Useroutletsgroups.query.filter_by(userid=userid,outletgroupid=outletgroupid).first() is None:
            return {'message': 'Relation between Userid %s and outletgroup %s doesn"t exists' % (userid, outletgroupid)}, BAD_REQUEST
        else:
            relation = Useroutletsgroups.query.filter_by(userid=userid,outletgroupid=outletgroupid).first()
            db.session.delete(relation)
            db.session.commit()
            return {'message': 'Relation between Userid %s and outletgroup %s is deleted' % (userid, outletgroupid)}


"""
    GET     /outlet_groups/user/groups/<int:id>         Returns the outletgroupings associatied with user
"""
class Usergroup(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('outletgroupid', type=int, required=True,
                                    help='No outletgroupid provided',
                                    location='json')
        super(Usergroup, self).__init__()

    def get(self, id):
        user = Userdetails.query.filter_by(id=id).first()
        if user is None:
            return {'message': 'User with id %s does not exist' %id }, NOT_FOUND
        username = user.username
        groups = Useroutletsgroups.query.filter_by(userid=id).all()

        return {'username: %s ' % username: 
                           [{'groupid': group.outletgroupid,
                           'location': url_for('groupings_group', id=group.outletgroupid,
                                               _external=True)}
                          for group in groups]}


# Login endpoint
"""
    GET     /outlet_groups/login            Generates an returns an authentication token
"""
class GroupingsloginAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        token = g.user.generate_auth_token(TOKEN_EXPIRATION)
        return {'token': token.decode('ascii'), 'duration': TOKEN_EXPIRATION}
