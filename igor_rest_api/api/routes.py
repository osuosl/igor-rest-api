#!/usr/bin/env python

from flask.ext.restful import Api

from igor_rest_api.api import errors
from igor_rest_api.api.auth.views import LoginAPI
from igor_rest_api.api.auth.views.users import (
    UserAPI, UsersAPI,
    UserMachinesAPI,
)
from igor_rest_api.api.ipmi.views import (
    MachineChassisAPI, MachineChassisPowerAPI,
    MachineSensorsAPI, MachineSensorAPI,
    MachineLanAPI, MachineLanChannelAPI,
    MachineLanAlertAPI, MachineLanChannelAlertAPI,
    MachineChassisPolicyAPI, MachineSelAPI, MachineSelTimeAPI,
    MachineSelRecordsAPI,
)
from igor_rest_api.api.machines.views import MachineAPI, MachinesAPI
from igor_rest_api.api.machines.views.permissions import (
    MachineUsersAPI,
    UserPermissionsMachineAPI,
)
from igor_rest_api.api.views import RootAPI

api = Api(errors=errors)

def add_resources(api, resources):
    for resource, url, endpoint in resources:
        api.add_resource(resource, url, endpoint=endpoint)


resources = [
    (RootAPI, '/', 'root'),
    (LoginAPI, '/login', 'login'),
    (UsersAPI, '/users', 'users'),
    (UserAPI,
        '/users/<string:username>',
        'user'),
    (UserMachinesAPI,
        '/users/<string:username>/machines',
        'user_machines'),
    (MachinesAPI,
        '/machines',
        'machines'),
    (MachineAPI,
        '/machines/<string:hostname>',
        'machine'),
    (UserPermissionsMachineAPI,
        '/users/<string:username>/machines/<string:hostname>/permissions',
        'user_machine'),
    (MachineUsersAPI, '/machines/<string:hostname>/users',
        'machine_users'),
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

add_resources(api, resources)