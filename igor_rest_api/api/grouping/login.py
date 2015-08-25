#!/usr/bin/env python
"""
This file provides methods to authenticate user using basic auth
"""
from functools import wraps

from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Resource

from igor_rest_api.api.constants import *

from .models import UserDetails

auth = HTTPBasicAuth()


# Authentication, writes g.user
@auth.verify_password
def validate_password(username_or_token, password):
    user = UserDetails.validate_auth_token(username_or_token)
    if not user:
        user = UserDetails.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


rootauth = HTTPBasicAuth()


@rootauth.verify_password
def validate_password(username_or_token, password):
    user = UserDetails.validate_auth_token(username_or_token)
    if not user:
        user = UserDetails.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
                return False
        elif user.username != 'root':
            return False
    g.user = user
    return True
