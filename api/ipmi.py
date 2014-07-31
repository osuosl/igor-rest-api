#!/usr/bin/env python

from constants import *
from flask import g, request
from flask.ext.restful import Resource, reqparse
from login import auth, permission_required
from pyipmi import make_bmc, IpmiError
from pyipmi.bmc import LanBMC
from pyipmi.sel import SELTimestamp, SELRecord
from utils import try_ipmi_command
from datetime import datetime

# IPMI Operations
class IPMIResource(Resource):
    decorators = [permission_required, auth.login_required]

    def __init__(self):
        self.bmc = make_bmc(LanBMC, hostname=g.machine.fqdn,
                            username=g.machine.username,
                            password=g.machine.password)
        super(IPMIResource, self).__init__()

"""
    GET     /machines/:hostname/chassis     View chassis status information
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
    GET     /machines/:hostname/chassis/power   View and set the chassis power
    POST    /machines/:hostname/chassis/power   status
            {'state': <valid state>}
"""
class MachineChassisPowerAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('state', type=str, required=True,
                                    help='No target power state provided',
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
        power_status = args['state']

        ipmi_response = try_ipmi_command(self.bmc.set_chassis_power,
                                         mode=power_status)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        return self.get(hostname)

"""
    GET     /machines/:hostname/chassis/policy      View and set the power
    POST    /machines/:hostname/chassis/policy      policy in the event of
            {'state': <valid state>}                power failure
"""
class MachineChassisPolicyAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('state', type=str, required=True,
                                    help='No target power policy provided',
                                    location='json')
        super(MachineChassisPolicyAPI, self).__init__()

    def get(self, hostname):
        chassisInfo = MachineChassisAPI()
        response, error_code = chassisInfo.get(hostname)

        if error_code != OK:
            return response

        return {'hostname': hostname,
                'policy': response['power_restore_policy']}

    def post(self, hostname):
        args = self.reqparse.parse_args()
        policy_status = args['state']

        ipmi_response = try_ipmi_command(self.bmc.set_chassis_policy,
                                         state=policy_status)
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

"""
    GET     /machines/:hostname/sel     View system event log information
"""
class MachineSelAPI(IPMIResource):

    def get(self, hostname):
        ipmi_response = try_ipmi_command(self.bmc.sel_info)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = ipmi_response[0].__dict__
        response['hostname'] = hostname

        # Fix non-JSON-serializable values
        response['last_add_time'] = str(response['last_add_time'])
        response['last_del_time'] = str(response['last_del_time'])

        return response, OK

"""
    GET     /machines/:hostname/sel/time    View and set the SEL clock's time
    POST    /machines/:hostname/sel/time    HH is in the 24-hour format
            {'time': 'MM/DD/YYYY HH:MM:SS'}
"""
class MachineSelTimeAPI(IPMIResource):

    def __init__(self):
        def validate_time(time):
            try:
                time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise ValueError('Invalid time format. ' + e.message)
            except:
                raise ValueError
            return datetime.strftime(time, '%m/%d/%Y %H:%M:%S')

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('time', type=validate_time, required=True,
                                    help='Missing or invalid time ' +
                                         '(YYYY-MM-DD hh:mm:ss)',
                                    location='json')
        super(MachineSelTimeAPI, self).__init__()

    def get(self, hostname):
        ipmi_response = try_ipmi_command(self.bmc.get_sel_time)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = ipmi_response[0].__dict__
        response['hostname'] = hostname
        response['time'] = str(response['time'])

        return response, OK

    def post(self, hostname):
        args = self.reqparse.parse_args()
        selTimestamp = SELTimestamp(timestamp=args['time'])
        ipmi_response = try_ipmi_command(self.bmc.set_sel_time,
                                         time=selTimestamp)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        return self.get(hostname)

"""
    GET     /machines/:hostname/sel/records?extended=True|False     View and
    DELETE  /machines/:hostname/sel/records                         update the
    POST    /machines/:hostname/sel/records                         list of
            {'records': [{'record_id': <record_id>,                 SEL records
                          'record_type': <record_type>,
                          'timestamp': <timestamp>,
                          'generator_id': <generator_id>,
                          'evm_rev': <evm_rev>,
                          'sensor_type': <sensor_type>,
                          'sensor_number': <sensor_number>,
                          'event_type': <event_type>,
                          'event_direction': <event_direction>,
                          'event_data': [0, 0, 0]},
                          ...]}
"""
class MachineSelRecordsAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('records', required=True,
                                    help='No records provided',
                                    location='json')
        super(MachineSelRecordsAPI, self).__init__()

    def get(self, hostname):
        extended = request.args.get('extended', 'False')

        if extended == 'True':
            ipmi_response = try_ipmi_command(self.bmc.sel_elist)
        else:
            ipmi_response = try_ipmi_command(self.bmc.sel_list)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = {'hostname': hostname,
                    'records': ipmi_response[0]}
        return response, OK
