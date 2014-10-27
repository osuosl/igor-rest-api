#!/usr/bin/env python

from flask.ext.restful import Api
from ipmi import MachineChassisAPI, MachineChassisPowerAPI
from ipmi import MachineSensorsAPI, MachineSensorAPI
from ipmi import MachineLanAPI, MachineLanChannelAPI
from ipmi import MachineLanAlertAPI, MachineLanChannelAlertAPI
from ipmi import MachineChassisPolicyAPI, MachineSelAPI, MachineSelTimeAPI
from ipmi import MachineSelRecordsAPI

from .login import LoginAPI, RootAPI
from .machines import MachineAPI, MachinesAPI
from .permissions import UserMachineAPI, UserMachinesAPI
from .permissions import MachineUserAPI, MachineUsersAPI
from .users import UserAPI, UsersAPI


resources = [
            (RootAPI, '/', 'root'),
            (LoginAPI, '/login', 'login'),
            (UsersAPI, '/users', 'users'),
            (UserAPI, '/users/<string:username>', 'user'),
            (MachinesAPI, '/machines', 'machines'),
            (MachineAPI, '/machines/<string:hostname>', 'machine'),
            (UserMachinesAPI, '/users/<string:username>/machines',
                'user_machines'),
            (UserMachineAPI,
                '/users/<string:username>/machines/<string:hostname>',
                'user_machine'),
            (MachineUsersAPI, '/machines/<string:hostname>/users',
                'machine_users'),
            (MachineUserAPI,
                '/machines/<string:hostname>/users/<string:username>',
                'machine_user'),
            (MachineChassisAPI,
                '/machines/<string:hostname>/chassis',
                'machine_chassis'),
            (MachineChassisPolicyAPI,
                '/machines/<string:hostname>/chassis/policy',
                'machine_chassis_policy'),
            (MachineChassisPowerAPI,
                '/machines/<string:hostname>/chassis/power',
                'machine_chassis_power'),
            (MachineSensorsAPI,
                '/machines/<string:hostname>/sensors',
                'machine_sensors'),
            (MachineSensorAPI,
                '/machines/<string:hostname>/sensors/<string:sensor>',
                'machine_sensor'),
            (MachineLanAPI,
                '/machines/<string:hostname>/lan',
                'machine_lan'),
            (MachineLanChannelAPI,
                '/machines/<string:hostname>/lan/<int:channel>',
                'machine_lan_channel'),
            (MachineLanAlertAPI,
                '/machines/<string:hostname>/lan/alert',
                'machine_lan_alert'),
            (MachineLanChannelAlertAPI,
                '/machines/<string:hostname>/lan/<int:channel>/alert',
                'machine_lan_channel_alert'),
            (MachineSelAPI,
                '/machines/<string:hostname>/sel',
                'machine_sel'),
            (MachineSelTimeAPI,
                '/machines/<string:hostname>/sel/time',
                'machine_sel_time'),
            (MachineSelRecordsAPI,
                '/machines/<string:hostname>/sel/records',
                'machine_sel_records')
            ]

def setup(app):
    igor_api = Api(app)
    for resourceClass, url, endpoint in resources:
        igor_api.add_resource(resourceClass, url, endpoint=endpoint)
