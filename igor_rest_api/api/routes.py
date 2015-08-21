#!/usr/bin/env python

from .auth.views import LoginAPI
from .ipmi.views import (
    MachineChassisAPI, MachineChassisPowerAPI,
    MachineSensorsAPI, MachineSensorAPI,
    MachineLanAPI, MachineLanChannelAPI,
    MachineLanAlertAPI, MachineLanChannelAlertAPI,
    MachineChassisPolicyAPI, MachineSelAPI, MachineSelTimeAPI,
    MachineSelRecordsAPI,
)
from .machines.views.machines import MachineAPI, MachinesAPI
from .machines.views.permissions import (
    UserMachineAPI, UserMachinesAPI,
    MachineUserAPI, MachineUsersAPI,
)
from .auth.views import UserAPI, UsersAPI
from .views import RootAPI
from .grouping.views import (
        PdudetailsAPI, PdudetailAPI,
        PduoutletsAPI, PduoutletAPI,
        GroupsAPI, GroupAPI,
        GroupoutletsAPI, UserpdusAPI
)
from .grouping.userviews import (
        GroupingusersAPI, GroupinguserAPI,
        Usergroups, GroupingsloginAPI,
        Usergroup
)
from .grouping.controlviews import (
        Groupcontrol, Outletcontrol,
        Pducontrol, Pduoutletcontrol
        )


resources = [
            (RootAPI, '/', 'root'),
            (PdudetailsAPI, '/pdu', 'groupings_pdus'),
            (PdudetailAPI, '/pdu/<string:ip>', 'groupings_pdu'),
            (PduoutletsAPI, '/outlets', 'groupings_outlets'),
            (Pducontrol, '/pdu/<string:pduip>/control', 'pdu_control'),
            (Pduoutletcontrol, '/pdu/<string:pduip>/<string:tower>/<int:outlet>/control', 'pdu_outlet_control'),
            (PduoutletAPI,
                '/outlets/<int:id>',
                'groupings_outlet'),
            (GroupsAPI, '/outlet_groups', 'groupings_groups'),
            (GroupAPI, '/outlet_groups/<int:groupid>', 'groupings_group'),
            (GroupoutletsAPI,
                '/outlet_groups/<int:groupid>/<int:outletid>',
                'groupings_groupings'),
            (UserpdusAPI,'/pdu/<int:pduid>/<int:userid>','user_pdus'),
            (Groupcontrol, '/outlet_groups/<int:groupid>/control', 'groupings_control'),
            (Outletcontrol, '/outlet/<int:outletid>/control', 'outlets_control'),
            (LoginAPI, '/login', 'login'),
            (UsersAPI, '/users', 'users'),
            (UserAPI, '/users/<string:username>', 'user'),
            (GroupingusersAPI, '/outlet_groups/users', 'groupingsusers'),
            (GroupinguserAPI,
                '/outlet_groups/users/<int:userid>',
                'groupingsuser'),
            (GroupingsloginAPI, '/outlet_groups/login', 'groupingslogin'),
            (Usergroups, '/outlet_groups/user/groups', 'groupings_users'),
            (Usergroup,
                '/outlet_groups/user/groups/<int:id>',
                'groupings_user'),
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


def setup(api):
    for resourceClass, url, endpoint in resources:
        api.add_resource(resourceClass, url, endpoint=endpoint)
