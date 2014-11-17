#!/usr/bin/env python

from flask import url_for
from flask.ext.restful import Resource, reqparse

from igor_rest_api.api.auth.login import auth
from igor_rest_api.api.constants import *
from igor_rest_api.api.machines.models import Machine
from igor_rest_api.api.models import db



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
                                    help='No hostname provided',
                                    location='json')
        self.reqparse.add_argument('fqdn', type=str, required=True,
                                    help='No FQDN provided',
                                    location='json')
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided',
                                    location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided',
                                    location='json')
        super(MachinesAPI, self).__init__()

    def get(self):
        machines = []
        for machine in Machine.query.all():
            machines.append(machine.hostname)
        return {'machines': [{'hostname': hostname,
                              'users': url_for('machine_users',
                                               hostname=hostname,
                                               _external=True),
                              'location': url_for('machine',
                                                  hostname=hostname,
                                                  _external=True)}
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
                    'users': url_for('machine_users', hostname=hostname,
                                     _external=True),
                    'location': url_for('machine', hostname=machine.hostname,
                                        _external=True)}, CREATED

"""
    GET     /machines/:hostname             Return details for the machine
    DELETE  /machines/:hostname             Delete the machine
    PUT     /machines/:hostname             Update FQDN/username/password
"""
class MachineAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('fqdn', type=str,
                                    help='No FQDN provided', location='json')
        self.reqparse.add_argument('username', type=str,
                                    help='No username provided',
                                    location='json')
        self.reqparse.add_argument('password', type=str,
                                    help='No password provided',
                                    location='json')
        super(MachineAPI, self).__init__()

    def get(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            return {'hostname': machine.hostname,
                    'fqdn': machine.fqdn,
                    'users': url_for('machine_users', hostname=hostname,
                                     _external=True),
                    'location': url_for('machine', hostname=hostname,
                                        _external=True)}

    def delete(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            machine.users = []
            db.session.add(machine)
            db.session.commit()
            db.session.delete(machine)
            db.session.commit()
            return {'message': 'Host %s deleted' % machine.hostname}

    def put(self, hostname):
        args = self.reqparse.parse_args()
        machine = Machine.query.filter_by(hostname=hostname).first()

        fqdn = args['fqdn'] if 'fqdn' in args else None
        username = args['username'] if 'username' in args else None
        password = args['password'] if 'password' in args else None

        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND
        else:
            if fqdn:
                machine.fqdn = fqdn
            if username:
                machine.username = username
            if password:
                machine.password = password
            db.session.add(machine)
            db.session.commit()
            return {'message': 'Updated entry for host %s' % hostname}
