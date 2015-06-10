#!/usr/bin/env python

from functools import wraps

from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Resource

from igor_rest_api.api.constants import *

from .models import Groupinguser

auth = HTTPBasicAuth()

# Authentication, writes g.user
@auth.verify_password
def validate_password(username_or_token, password):
    user = Groupinguser.validate_auth_token(username_or_token)
    if not user:
        user = Groupinguser.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True
