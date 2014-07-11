#!/usr/bin/env python

from constants import *
from pyipmi import IpmiError

# Utility functions
def try_ipmi_command(command, **kwargs):
    try:
        response = command(**kwargs), OK
    except IpmiError as error:
        response = error.message, BAD_REQUEST
    return response
