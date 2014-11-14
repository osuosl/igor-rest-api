#!/usr/bin/env python

from functools import wraps

from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Resource

from igor_rest_api.api.constants import *
from igor_rest_api.api.machines.models import Machine

from .models import User

auth = HTTPBasicAuth()

# Authentication, writes g.user
@auth.verify_password
def validate_password(username_or_token, password):
    user = User.validate_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True

# Authorization for the IPMI operations
# Requires g.user and hostname, writes g.machine
def permission_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = g.user

        hostname = kwargs['hostname']
        machine = Machine.query.filter_by(hostname=hostname).first()
        if not machine:
            return {'message': 'Host %s does not exist' % hostname}, NOT_FOUND

        if not user in machine.users:
            return {'message': 'User %s does not have permission for host %s'
                    % (user.username, hostname)}, FORBIDDEN

        g.machine = machine
        return f(*args, **kwargs)
    return decorated

