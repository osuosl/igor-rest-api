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
        return response, OK

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
        chassisInfo = MachineChassisAPI()
        response, error_code = chassisInfo.get(hostname)

        if error_code != OK:
            return response

        return {'hostname': hostname, 'power_on': response['power_on']}

    def post(self, hostname):
        args = self.reqparse.parse_args()
        power_status = args['power']

        ipmi_response = try_ipmi_command(self.bmc.set_chassis_power,
                                         mode=power_status)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        return self.get(hostname)

"""
    GET     /machines/:hostname/sensors         Returns all sensor readings
"""
class MachineSensorsAPI(IPMIResource):

    def get(self, hostname):
        """
        ipmi_response = try_ipmi_command(self.bmc.sdr_list)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST
        """
        return {'message': 'not implemented'}, NOT_IMPLEMENTED
        

"""
    GET     /machines/:hostname/sensors/:string     Returns the readings
                                                    for all sensors matching
                                                    the provided :string
"""
class MachineSensorAPI(IPMIResource):

    def get(self, hostname, string):
        """
        machineSensorsAPI = MachineSensorsAPI()
        response, error_code = MachineSensorsAPI.get()

        if error_code != OK:
            return response
        """
        return {'message': 'not implemented'}, NOT_IMPLEMENTED

"""
    GET     /machines/:hostname/lan         View lan channel information
"""
class MachineLanAPI(IPMIResource):

    def get(self, hostname, channel=None):
        ipmi_response = try_ipmi_command(self.bmc.lan_print, channel=channel)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST
        
        response = ipmi_response[0].__dict__
        return response, OK

"""
    GET     /machines/:hostname/lan/alert   View lan alert channel information
"""
class MachineLanAlertAPI(IPMIResource):

    def get(self, hostname, channel=None):
        """
        ipmi_response = try_ipmi_command(self.bmc.alert_print, channel=channel)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = ipmi_response[0].__dict__
        return response, OK
        """
        return {'message': 'endpoint not implemented'}, NOT_IMPLEMENTED

"""
    GET     /machines/:hostname/lan/:channel                View and set lan
    POST    /machines/:hostname/lan/:channel                channel information
            {'command': '<command>', 'param': '<param>'}
"""
class MachineLanChannelAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('command', type=str, required=True,
                                    help='No command provided to lan set',
                                    location='json')
        self.reqparse.add_argument('param', type=str, required=True,
                                    help='No param provided to lan set',
                                    location='json')
        super(MachineLanChannelAPI, self).__init__()

    def get(self, hostname, channel):
        machineLanAPI = MachineLanAPI()
        ipmi_response, error_code = machineLanAPI.get(hostname, channel=channel)
        return ipmi_response, error_code

    def post(self, hostname, channel):
        args = self.reqparse.parse_args()
        command = args['command']
        param = args['param']

        ipmi_response = try_ipmi_command(self.bmc.lan_set, channel=channel,
                                         command=command, param=param)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': 'bad lan set command'}, \
                   BAD_REQUEST

        return self.get(hostname, channel)

"""
    GET     /machines/:hostname/lan/:channel/alert      View and set lan alert
    POST    /machines/:hostname/lan/:channel/alert      channel information
            {'command': '<command>', 'param': '<param>'}
"""
class MachineLanChannelAlertAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('command', type=str, required=True,
                                    help='No command provided to lan set',
                                    location='json')
        self.reqparse.add_argument('param', type=str, required=True,
                                    help='No param provided to lan set',
                                    location='json')
        super(MachineLanChannelAlertAPI, self).__init__()

    def get(self, hostname, channel):
        machineLanAlertAPI = MachineLanAlertAPI()
        ipmi_response, error_code = machineLanAlertAPI.get(hostname,
                                                           channel=channel)
        return ipmi_response, error_code

    def post(self, hostname, channel):
        args = self.reqparse.parse_args()
        command = args['command']
        param = args['param']

        """
        ipmi_response = try_ipmi_command(self.bmc.lan_set, channel=channel,
                                         command=command, param=param)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': 'bad lan set command'}, \
                   BAD_REQUEST

        return self.get(hostname, channel)
        """
        return {'message': 'endpoint not implemented'}, NOT_IMPLEMENTED
