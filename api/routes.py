#!/usr/bin/env python

from api import app
from flask.ext.restful import Api
from login import LoginAPI, RootAPI
from users import UserAPI, UsersAPI
from machines import MachineAPI, MachinesAPI
from permissions import UserMachineAPI, UserMachinesAPI
from permissions import MachineUserAPI, MachineUsersAPI
from ipmi import MachineChassisAPI, MachineChassisPowerAPI
from ipmi import MachineSensorsAPI, MachineLanAPI, MachineLanChannelAPI
from ipmi import MachineLanAlertAPI, MachineLanChannelAlertAPI
from ipmi import MachineChassisPolicyAPI, MachineSelAPI

igor_api = Api(app)

igor_api.add_resource(RootAPI, '/', endpoint='root')
igor_api.add_resource(LoginAPI, '/login', endpoint='login')
igor_api.add_resource(UsersAPI, '/users', endpoint='users')
igor_api.add_resource(UserAPI, '/users/<string:username>', endpoint='user')
igor_api.add_resource(MachinesAPI, '/machines', endpoint='machines')
igor_api.add_resource(MachineAPI, '/machines/<string:hostname>',
                      endpoint='machine')
igor_api.add_resource(UserMachinesAPI, '/users/<string:username>/machines',
                      endpoint='user_machines')
igor_api.add_resource(UserMachineAPI,
                      '/users/<string:username>/machines/<string:hostname>',
                      endpoint='user_machine')
igor_api.add_resource(MachineUsersAPI, '/machines/<string:hostname>/users',
                      endpoint='machine_users')
igor_api.add_resource(MachineUserAPI,
                      '/machines/<string:hostname>/users/<string:username>',
                      endpoint='machine_user')
igor_api.add_resource(MachineChassisAPI,
                      '/machines/<string:hostname>/chassis',
                      endpoint='machine_chassis')
igor_api.add_resource(MachineChassisPolicyAPI,
                      '/machines/<string:hostname>/chassis/policy',
                      endpoint='machine_chassis_policy')
igor_api.add_resource(MachineChassisPowerAPI,
                      '/machines/<string:hostname>/chassis/power',
                      endpoint='machine_chassis_power')
igor_api.add_resource(MachineSensorsAPI,
                      '/machines/<string:hostname>/sensors',
                      endpoint='machine_sensors')
igor_api.add_resource(MachineLanAPI,
                      '/machines/<string:hostname>/lan',
                      endpoint='machine_lan')
igor_api.add_resource(MachineLanChannelAPI,
                      '/machines/<string:hostname>/lan/<int:channel>',
                      endpoint='machine_lan_channel')
igor_api.add_resource(MachineLanAlertAPI,
                      '/machines/<string:hostname>/lan/alert',
                      endpoint='machine_lan_alert')
igor_api.add_resource(MachineLanChannelAlertAPI,
                      '/machines/<string:hostname>/lan/<int:channel>/alert',
                      endpoint='machine_lan_channel_alert')
igor_api.add_resource(MachineSelAPI,
                      '/machines/<string:hostname>/sel',
                      endpoint='machine_sel')
