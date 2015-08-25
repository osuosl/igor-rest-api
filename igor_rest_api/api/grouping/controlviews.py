#!/usr/bin/env python

from flask import url_for, g
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from igor_rest_api.api.grouping.login import auth
from igor_rest_api.api.constants import *
from igor_rest_api.api.grouping.models import (
        Group, PduDetails, Outlets, GroupOutlets,
        UserOutletsGroups, UserPdus)
from igor_rest_api.api.grouping.utils import (
        query_group, outlet_details,
        check_outlet_permission)
from igor_rest_api.db import db
from pudmaster import Pdu_obj


"""
    GET     /outlet_groups/<int:groupid>/control       Returns the Status of Outlets belonging to the outletgrouping
    POST    /outlet_groups/<int:groupid>/control  {'action': Status } Changes the Status of outlets belonging to outletgrouping
"""


class Groupcontrol(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('action', type=str, required=True,
                                   help='No action provided',
                                   location='json')
        super(Groupcontrol, self).__init__()

    def get(self, groupid):
        if g.user.username == 'root':
            outlets = query_group(groupid)

        else:
            role = UserOutletsGroups.query.filter_by(userid=g.user.id,
                                                     outletgroupid=groupid).first()
            if role is None:
                return {'message': 'User does not have necessary permission'}
            else:
                outlets = query_group(groupid)

        states = []
        amperages = []
        for outlet in outlets:
            pdu = Pdu_obj(outlet[0], 161, outlet[1])
            state = pdu.get_outlet_status(outlet[2], outlet[3])
            amperage = pdu.get_outlet_amperage(outlet[2], outlet[3])

            if state == 'Error':
                states.append("unable to get data")
            else:
                states.append(state)

            if amperage == 'Error':
                amperages.append('unable to get data')
            else:
                amperages.append(amperage)

        state_dict = {}
        for i in range(len(outlets)):
            state_dict[str(outlets[i][0])+" "+str(outlets[i][2])+" "+str(outlets[i][3])] = states[i]

        amperage_dict = {}
        for i in range(len(outlets)):
            amperage_dict[str(outlets[i][0])+" "+str(outlets[i][2])+" "+str(outlets[i][3])] = amperages[i]
        return {'Status': state_dict, 'amperages': amperage_dict}

    def post(self, groupid):
        args = self.reqparse.parse_args()

        status = args['action']
        if g.user.username == 'root':
            outlets = query_group(groupid)

        else:
            role = UserOutletsGroups.query.filter_by(userid=g.user.id,
                                                     outletgroupid=groupid).first()
            if role is None:
                return {'message': 'User does not have necessary permission'}
            else:
                outlets = query_group(groupid)

        states = []
        for outlet in outlets:
            pdu = Pdu_obj(outlet[0], 161, outlet[1])
            ret_value = pdu.change_state(outlet[2], outlet[3], status)
            if 'No SNMP response received' in str(ret_value):
                states.append("unable to connect to pdu")
            else:
                states.append("changed state")

        state_dict = {}
        for i in range(len(outlets)):
            state_dict[str(outlets[i][0])+" "+str(outlets[i][2])+" "+str(outlets[i][3])] = states[i]

        return {'Status': state_dict}


"""
    GET     /outlet/<int:outletid>/control                       Returns the Status of outlet
    POST    /outlet/<int:outletid>/control {'action': status }   Changes the Status of outlet
"""


class Outletcontrol(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('action', type=str, required=True,
                                   help='No action provided',
                                   location='json')
        super(Outletcontrol, self).__init__()

    def get(self, outletid):
        if g.user.username == 'root':
            outlet = outlet_details(outletid)
        else:
            role = check_outlet_permission(g.user.id, outletid)
            if role is False:
                return {'message': 'User does not have neccesary permission'}
            else:
                outlet = outlet_details(outletid)
        pdu = Pdu_obj(outlet[0], 161, outlet[1])
        state = pdu.get_outlet_status(outlet[2], outlet[3])
        amperage = pdu.get_outlet_amperage(outlet[2], outlet[3])

        states = []
        if state == 'Error':
            states.append("unable to get data")
        else:
            states.append(state)

        if amperage == 'Error':
            amperage = 'unable to fetch data'
        else:
            amperage = amperage

        state_dict = {}
        state_dict[str(outlet[0])+" "+str(outlet[2])+" "+str(outlet[3])] = states[0]
        state_dict['amperage'] = amperage

        return {'Status': state_dict}

    def post(self, outletid):
        args = self.reqparse.parse_args()

        status = args['action']
        if g.user.username == 'root':
            outlet = outlet_details(outletid)
        else:
            role = check_outlet_permission(g.user.id, outletid)
            if role is False:
                return {'message': 'User does not have neccesary permission'}
            else:
                outlet = outlet_details(outletid)

        pdu = Pdu_obj(outlet[0], 161, outlet[1])
        states = []
        ret_value = pdu.change_state(outlet[2], outlet[3], status)
        if 'No SNMP response received' in str(ret_value):
            states.append("unable to connect to pdu")
        else:
            states.append("changed state")
        state_dict = {}
        state_dict[str(outlet[0])+" "+str(outlet[2])+" "+str(outlet[3])] = states[0]

        return {'Status': state_dict}

"""
    GET     /pdu/<string:pduip>/control                       Returns the Status of Pdu
    POST    /pdu/<string:pduip>/control {'action': status }   Changes the Status of Pdu
"""


class Pducontrol(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('action', type=str, required=True,
                                   help='No action provided',
                                   location='json')
        super(Pducontrol, self).__init__()

    def get(self, pduip):
        if g.user.username == 'root':
            pdu = PduDetails.query.filter_by(ip=pduip).first()
            if pdu is None:
                return {'Error': 'pdu doesn"t exist'}
            else:
                pdu_access_string = pdu.access_string
        else:
            pdu = PduDetails.query.filter_by(ip=pduip).first()
            if pdu is None:
                return {'Error': 'pdu doesn"t exist'}
            relation = UserPdus.query.filter_by(userid=g.user.id, pduid=pdu.id).first()
            if relation is None:
                return {'message': 'User does not have neccesary permission'}
            pdu_access_string = pdu.access_string

        pdu = Pdu_obj(pduip, 161, pdu_access_string)
        try:
            status, name = pdu.complete_status()
        except ValueError:
            return {'error': 'Unable to get data'}

        if status == "Error":
            return {'error': 'Unable to get data'}

        amperage = pdu.get_amperage_details()
        status_dict = {}
        for i in range(len(status)):
            status_dict[name[i]] = status[i]
        amperage_dict = {}
        amperage_dict['tower_A'] = amperage[0]
        amperage_dict['tower_B'] = amperage[1]
        return {'status': status_dict, 'amperage': amperage_dict}

    def post(self, pduip):
        args = self.reqparse.parse_args()

        status = args['action']
        if g.user.username == 'root':
            pdu = PduDetails.query.filter_by(ip=pduip).first()
            if pdu is None:
                return {'Error': 'pdu doesn"t exist'}
            else:
                pdu_access_string = pdu.access_string
        else:
            pdu = PduDetails.query.filter_by(ip=pduip).first()
            if pdu is None:
                return {'Error': 'pdu doesn"t exist'}
            relation = UserPdus.query.filter_by(userid=g.user.id, pduid=pdu.id).first()
            if relation is None:
                return {'message': 'User does not have neccesary permission'}
            pdu_access_string = pdu.access_string

        pdu = Pdu_obj(pduip, 161, pdu_access_string)

"""
    GET     /pdu/<string:pduip>/<string:tower>/<int:outlet>/control
            Returns the Status of Pdu
    POST    /pdu/<string:pduip>/<string:tower>/<int:outlet>/control
            {'action': status }
            Changes the Status of Pdu
"""


class Pduoutletcontrol(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('action', type=str, required=True,
                                   help='No action provided',
                                   location='json')
        super(Pduoutletcontrol, self).__init__()

    def get(self, pduip, tower, outlet):
        if g.user.username == 'root':
            pdu = PduDetails.query.filter_by(ip=pduip).first()
            if pdu is None:
                return {'Error': 'pdu doesn"t exist'}
            else:
                pdu_access_string = pdu.access_string
        else:
            pdu = PduDetails.query.filter_by(ip=pduip).first()
            if pdu is None:
                return {'Error': 'pdu doesn"t exist'}
            relation = UserPdus.query.filter_by(userid=g.user.id, pduid=pdu.id).first()
            if relation is None:
                return {'message': 'User does not have neccesary permission'}
            pdu_access_string = pdu.access_string

        pdu = Pdu_obj(pduip, 161, pdu_access_string)
        state = pdu.get_outlet_status(tower, outlet)
        amperage = pdu.get_outlet_amperage(tower, outlet)

        if state == 'Error':
            state = 'Unable to fetch data'
        if amperage == 'Error':
            amperage = 'unable to fetch amperage'

        return {'state': state, 'amperage': amperage}

    def post(self, pduip, tower, outlet):
        args = self.reqparse.parse_args()

        status = args['action']
        if g.user.username == 'root':
            pdu = PduDetails.query.filter_by(ip=pduip).first()
            if pdu is None:
                return {'Error': 'pdu doesn"t exist'}
            else:
                pdu_access_string = pdu.access_string
        else:
            pdu = PduDetails.query.filter_by(ip=pduip).first()
            if pdu is None:
                return {'Error': 'pdu doesn"t exist'}
            relation = UserPdus.query.filter_by(userid=g.user.id, pduid=pdu.id).first()
            if relation is None:
                return {'message': 'User does not have neccesary permission'}
            pdu_access_string = pdu.access_string

        pdu = Pdu_obj(pduip, 161, pdu_access_string)
        ret_value = pdu.change_state(tower, outlet, status)
        if 'No SNMP response received' in str(ret_value):
            return {'Error': 'unable to connect to pdu'}
        else:
            return {'Success': 'Changed state'}
