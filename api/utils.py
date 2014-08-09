#!/usr/bin/env python

from constants import *
from pyipmi import IpmiError

# Utility functions
def try_ipmi_command(ipmi_command, *args, **kwargs):
    try:
        response = ipmi_command(*args, **kwargs), OK
    except IpmiError as error:
        response = error.message, BAD_REQUEST
    return response
