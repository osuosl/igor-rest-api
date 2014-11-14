#!/usr/bin/env python

from pyipmi import IpmiError

from igor_rest_api.api.constants import *

# Utility functions
def try_ipmi_command(ipmi_command, *args, **kwargs):
    try:
        response = ipmi_command(*args, **kwargs), OK
    except IpmiError as error:
        response = error.message, BAD_REQUEST
    return response
