#!/usr/bin/env python

from flask import url_for
from flask.ext.restful import Resource, reqparse, fields, marshal_with

from igor_rest_api.api.auth.login import auth
from igor_rest_api.api.constants import *
from igor_rest_api.api.exceptions import (
    ResourceAlreadyExists, ResourceDoesNotExist,
)
from igor_rest_api.api.machines.models import Machine
from igor_rest_api.api.models import db


machine_fields = {
    'id': fields.Integer,
    'hostname': fields.String,
    'fqdn': fields.String,
}

machine_fields_with_users = machine_fields.copy()
machine_fields_with_users.update({
    'users': fields.Nested({
        'id': fields.Integer,
        'username': fields.String
    }),
})

# Machine management endpoints
class MachinesAPI(Resource):
    decorators = [auth.login_required]

    machines_fields = {
        'machines': fields.Nested(machine_fields_with_users)
    }

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

    @marshal_with(machines_fields)
    def get(self):
        return {'machines':Machine.query.all()}

    @marshal_with(machine_fields)
    def post(self):
        args = self.reqparse.parse_args()

        hostname = args['hostname']
        fqdn     = args['fqdn']
        username = args['username']
        password = args['password']

        if Machine.query.filter_by(hostname=hostname).first() is not None:
            raise ResourceAlreadyExists()
        else:
            machine = Machine(hostname, fqdn, username, password)
            db.session.add(machine)
            db.session.commit()
            return machine

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

    @marshal_with(machine_fields_with_users)
    def get(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            raise ResourceDoesNotExist('Host %s does not exist' % hostname)
        else:
            return machine

    @marshal_with(machine_fields)
    def delete(self, hostname):
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            raise ResourceDoesNotExist('Host %s does not exist' % hostname)
        else:
            db.session.delete(machine)
            db.session.commit()
            return machine

    @marshal_with(machine_fields)
    def put(self, hostname):
        args = self.reqparse.parse_args()
        # remove all empty values from the args
        args = { k:v for k, v in args.items() if v is not None }

        # Update the machine
        updated = Machine.query.filter_by(hostname=hostname).update(args)
        db.session.commit()

        if not updated:
            raise ResourceDoesNotExist('Host %s does not exist' % hostname)
        else:
            machine = Machine.query.filter_by(**args).first()
            return machine
