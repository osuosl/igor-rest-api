#!/usr/bin/env python

from flask import url_for
from flask.ext.restful import Resource

from igor_rest_api.api.auth.login import auth
from igor_rest_api.api.auth.models import User
from igor_rest_api.api.constants import *
from igor_rest_api.api.models import db

from ..models import Machine

class UserPermissionsMachineAPI(Resource):
    """
    GET, PUT, DELETE    /users/:username/machines/:hostname/permissions
    """
    decorators = [auth.login_required]


    def get(self, username, hostname):
        """
        Returns 200 or 404, depending on :username's access to :hostname
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if machine in user.machines:
            return {'username': username,
                    'hostname': hostname,
                    'location': url_for('machine', hostname=hostname,
                                        _external=True)}
        else:
            return {'message': 'User %s does not have permission for host %s'
                    % (username, hostname)}, NOT_FOUND

    def put(self, username, hostname):
        """
        Adds :username-:hostname entry to the permissions table
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if machine not in user.machines:
            user.machines.append(machine)
            db.session.add(user)
            db.session.commit()

        return {'message': 'Created permission for user %s to host %s'
                % (username, hostname)}, CREATED

    def delete(self, username, hostname):
        """"
        Deletes :username-:hostname entry in the permissions table
        """

        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if machine in user.machines:
            user.machines.remove(machine)
            db.session.add(user)
            db.session.commit()

            return {'message': 'Deleted permission for user %s to host %s'
                    % (username, hostname)}
        else:
            return {'message': 'User %s does not have permission for host %s'
                    % (username, hostname)}, NOT_FOUND


class MachineUsersAPI(Resource):
    """
    GET     /machines/:hostname/users
    """

    decorators = [auth.login_required]

    def get(self, hostname):
        """
        Returns the list of users with access to :hostname
        """
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        return {'hostname': machine.hostname,
                'users': [{'username': user.username,
                           'location': url_for('user', username=user.username,
                                               _external=True)}
                            for user in machine.users]}


