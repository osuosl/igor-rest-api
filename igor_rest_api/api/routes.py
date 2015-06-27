#!/usr/bin/env python

from .auth.views import LoginAPI
from .snmp.views import SNMPLoginAPI
from .ipmi.views import (
    MachineChassisAPI, MachineChassisPowerAPI,
    MachineSensorsAPI, MachineSensorAPI,
    MachineLanAPI, MachineLanChannelAPI,
    MachineLanAlertAPI, MachineLanChannelAlertAPI,
    MachineChassisPolicyAPI, MachineSelAPI, MachineSelTimeAPI,
    MachineSelRecordsAPI,
)
from .snmpcontrol.views import Pdustatus, OutletStatus
from .machines.views.machines import MachineAPI, MachinesAPI
from .pdus.views.pdus import PduAPI, PdusAPI
from .machines.views.permissions import (
    UserMachineAPI, UserMachinesAPI,
    MachineUserAPI, MachineUsersAPI,
)
from .pdus.views.permissions import (
        UserPduAPI, UserPdusAPI,
        PduUserAPI, PduUsersAPI,
)
from .auth.views import UserAPI, UsersAPI
from .snmp.views import SNMPUserAPI, SNMPUsersAPI
from .views import RootAPI
from .grouping.views import (
        PdudetailsAPI, PdudetailAPI,
        PduoutletsAPI, PduoutletAPI,
        GroupsAPI, GroupAPI,
        GroupoutletsAPI,
)
from .grouping.userviews import (
        GroupingusersAPI, GroupinguserAPI, 
        Usergroups, GroupingsloginAPI,
        Usergroup
)
from .grouping.controlviews import Groupcontrol, Outletcontrol


resources = [
            (RootAPI, '/', 'root'),
            (PdudetailsAPI,'/outlet_groups/pdu','groupings_pdus'),
            (PdudetailAPI,'/outlet_groups/pdu/<string:ip>','groupings_pdu'),
            (PduoutletsAPI,'/outlet_groups/outlets','groupings_outlets'),
            (PduoutletAPI,'/outlet_groups/outlets/<int:id>','groupings_outlet'),
            (GroupsAPI,'/outlet_groups/groups','groupings_groups'),
            (GroupAPI,'/outlet_groups/groups/<int:id>','groupings_group'),
            (GroupoutletsAPI,'/outlet_groups/groupings','groupings_groupings'),
            (Groupcontrol,'/group/<int:groupid>','groupings_control'),
            (Outletcontrol,'/outlet/<int:outletid>','outlets_control'),
            (LoginAPI, '/login', 'login'),
            (SNMPLoginAPI, '/snmplogin', 'snmplogin'),
            (UsersAPI, '/users', 'users'),
            (UserAPI, '/users/<string:username>', 'user'),
            (SNMPUsersAPI, '/snmpusers', 'snmpusers'),
            (SNMPUserAPI, '/snmpusers/<string:username>', 'snmpuser'),
            (GroupingusersAPI, '/outlet_groups/users', 'groupingsusers'),
            (GroupinguserAPI, '/outlet_groups/users/<string:username>', 'groupingsuser'),
            (GroupingsloginAPI, '/outlet_groups/login', 'groupingslogin'),
            (Usergroups, '/outlet_groups/user/groups', 'groupings_users'),
            (Usergroup, '/outlet_groups/user/groups/<int:id>', 'groupings_user'),
            (MachinesAPI, '/machines', 'machines'),
            (MachineAPI, '/machines/<string:hostname>', 'machine'),
            (PdusAPI, '/pdus', 'pdus'),
            (PduAPI, '/pdus/<string:ip>', 'pdu'),
            (Pdustatus, '/pdu/<string:ip>/status', 'pdustatus'),
            (OutletStatus, '/pdu/<string:ip>/<string:tower>/<int:outlet>', 'Outletstatus'),
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
            (UserPdusAPI, '/snmpusers/<string:username>/pdus',
                'user_pdus'),
            (UserPduAPI,
                '/snmpusers/<string:username>/pdus/<string:ip>',
                'user_pdu'),
            (PduUsersAPI, '/pdus/<string:ip>/users',
                'pdu_users'),
            (PduUserAPI,
                '/pdus/<string:ip>/users/<string:username>',
                'pdu_user'),
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
