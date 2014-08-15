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
from urllib import unquote_plus

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
    POST    /machines/:hostname/sensors
            {'sensors': [{'id': <sensor_id>}, ...]}

"""
class MachineSensorsAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensors', required=True,
                                    type=lambda x: [i for i in x],
                                    help='No sensor IDs provided',
                                    location='json')
        super(MachineSensorsAPI, self).__init__()

    def get(self, hostname):
        ipmi_response = try_ipmi_command(self.bmc.sensor_list)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = {'hostname': hostname,
                    'records': ipmi_response[0]}

        return response, OK

    def post(self, hostname):
        args = self.reqparse.parse_args()
        ids = [sensor['id'] for sensor in args['sensors']]

        ipmi_response = try_ipmi_command(self.bmc.sensor_get, *ids)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = {'sensors': [sensor.__dict__ for sensor
                                in ipmi_response[0]]}

        return response, OK

"""
    GET     /machines/:hostname/sensors/:sensor
    POST    /machines/:hostname/sensors/:sensor
            {'threshold': '<setting>|lower|upper',
             'values': [<value>, ...]}
"""
class MachineSensorAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('threshold', required=True,
                                    type=str,
                                    help='No threshold setting provided',
                                    location='json')
        self.reqparse.add_argument('values', required=True,
                                    type=lambda x: [i for i in x],
                                    help='No theshold value(s) provided',
                                    location='json')
        super(MachineSensorAPI, self).__init__()

    def get(self, hostname, sensor):
        ipmi_response = try_ipmi_command(self.bmc.sensor_get, sensor)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = {'sensors': [sensor.__dict__ for sensor
                                in ipmi_response[0]]}

        return response, OK

    def post(self, hostname, sensor):
        args = self.reqparse.parse_args()
        threshold = args['threshold']
        values = [str(i) for i in args['values']]
        sensor = unquote_plus(sensor)

        ipmi_response = try_ipmi_command(self.bmc.sensor_thresh,
                                         sensor=sensor,
                                         threshold=threshold,
                                         values=values)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = {'message': ipmi_response[0]}

        return response, OK

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
        ipmi_response = try_ipmi_command(self.bmc.lan_alert_print,
                                         channel=channel)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = {'hostname': hostname,
                    'alerts': [alert.__dict__ for alert in ipmi_response[0]]}
        return response, OK

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
        self.reqparse.add_argument('dest', type=str, required=True,
                                    help='No alert destination for lan set',
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
        dest = args['dest']

        ipmi_response = try_ipmi_command(self.bmc.lan_alert_set,
                                         channel=channel, command=command,
                                         alert_destination=dest, param=param)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': 'bad lan set command'}, \
                   BAD_REQUEST

        return self.get(hostname, channel)

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

"""View the list of SEL records

    GET     /machines/:hostname/sel/records?extended=True|False
    DELETE  /machines/:hostname/sel/records
    POST    /machines/:hostname/sel/records
            {'records': [{'id': <record_id>, ...}]}
"""
class MachineSelRecordsAPI(IPMIResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('records', required=True,
                                    type=lambda x: [i for i in x],
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

    def delete(self, hostname):
        ipmi_response = try_ipmi_command(self.bmc.sel_clear)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        return self.get(hostname)

    def post(self, hostname):
        args = self.reqparse.parse_args()
        ids = [record['id'] for record in args['records']]

        ipmi_response = try_ipmi_command(self.bmc.sel_get,
                                         *ids)
        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = {'hostname': hostname,
                    'records': ipmi_response[0]}

        return response, OK

"""Get and delete SEL record entries

    GET     /machines/:hostname/sel/records/:id
    DELETE  /machines/:hostname/sel/records/:id
"""
class MachineSelRecordAPI(IPMIResource):

    def get(self, hostname, id):
        ipmi_response = try_ipmi_command(self.bmc.sel_get, id)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        response = {'hostname': hostname,
                    'records': ipmi_response[0]}

        return response, OK

    def delete(self, hostname, id):
        ipmi_response = try_ipmi_command(self.bmc.sel_delete, id)

        if ipmi_response[-1] != OK:
            return {'hostname': hostname, 'message': ipmi_response[0]}, \
                   BAD_REQUEST

        return {'hostname': hostname, 'message': 'Deleted record ' + id}, OK
