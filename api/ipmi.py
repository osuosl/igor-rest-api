#!/usr/bin/env python

from constants import *
from flask import g
from flask.ext.restful import Resource, reqparse
from login import auth, permission_required
from pyipmi import make_bmc, IpmiError
from pyipmi.bmc import LanBMC
from utils import try_ipmi_command

# IPMI Operations
class IPMIResource(Resource):
    decorators = [permission_required, auth.login_required]

    def __init__(self):
        self.bmc = make_bmc(LanBMC, hostname=g.machine.fqdn,
                            username=g.machine.username,
                            password=g.machine.password)
        super(IPMIResource, self).__init__()

"""
    GET     /machines/:hostname/chassis     Gets the chassis status
"""
class MachineChassisAPI(IPMIResource):

    def get(self, hostname):
        ipmi_response = try_ipmi_command(self.bmc.get_chassis_status)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = ipmi_response[0].__dict__
        response['hostname'] = hostname
        return response

"""
    GET     /machines/:hostname/chassis/power     Gets the chassis power status
    POST    /machines/:hostname/chassis/power
            {'power': 'on'|'off'|'cycle}          Sets the chassis power
"""
class MachineChassisPowerAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('power', type=str, required=True,
                                    help='No power status provided',
                                    location='json')
        super(MachineChassisPowerAPI, self).__init__()

    def get(self, hostname):
        ipmi_response = try_ipmi_command(self.bmc.get_chassis_status)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        power_on = ipmi_response[0].power_on
        if power_on:
            power_status = 'on'
        else:
            power_status = 'off'

        return {'hostname': hostname, 'power': power_status}

    def post(self, hostname):
        args = self.reqparse.parse_args()
        power_status = args['power']

        ipmi_response = try_ipmi_command(self.bmc.set_chassis_power,
                                         mode=power_status)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        return {'hostname': hostname,
                'message': 'Power status set to %s' % power_status}
