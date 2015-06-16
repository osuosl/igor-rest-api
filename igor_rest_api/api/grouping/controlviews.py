#!/usr/bin/env python

from flask import url_for, g
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from igor_rest_api.api.grouping.login import auth
from igor_rest_api.api.constants import *
from igor_rest_api.api.grouping.models import Group, Pdudetails, Outlets, Groupoutlets, Useroutletsgroups
from igor_rest_api.api.grouping.utils import query_group, outlet_details, check_outlet_permission
from igor_rest_api.db import db
from pudmaster import Pdu_obj


class Groupcontrol(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('status', type=str, required=True,
                                    help='No status provided',
                                    location='json')
        super(Groupcontrol, self).__init__()

    def get(self, groupid):
        if g.user.username == 'root':
            outlets = query_group(groupid)

        else :
            role = Useroutletsgroups.query.filter_by(userid=g.user.id,outletgroupid=groupid).first()
            if role is None:
                return {'message': 'User does not have necessary permission'}
            else:
                outlets = query_group(groupid)

        states = []
        for outlet in outlets:
            pdu = Pdu_obj(outlet[0],161,outlet[1])
            state = pdu.get_outlet_status(outlet[2],outlet[3])
            
            if state == 'Error':
                states.append("unable to get data")
            else:
                states.append(state)

        state_dict = {}
        for i in range(len(outlets)):
            state_dict[str(outlets[i][0])+" "+str(outlets[i][2])+" "+str(outlets[i][3])] = states[i]
        
        return {'Status': state_dict}


    def post(self, groupid):
        args = self.reqparse.parse_args()

        status = args['status']
        if g.user.username == 'root':
            outlets = query_group(groupid)

        else :
            role = Useroutletsgroups.query.filter_by(userid=g.user.id,outletgroupid=groupid).first()
            if role is None:
                return {'message': 'User does not have necessary permission'}
            else:
                outlets = query_group(groupid)

        states = []
        for outlet in outlets:
            pdu = Pdu_obj(outlet[0],161,outlet[1])
            ret_value = pdu.change_state(outlet[2],outlet[3],status)
            if 'No SNMP response received' in str(ret_value):
                states.append("unable to connect to pdu")
            else:
                states.append("chnaged state")

        state_dict = {}
        for i in range(len(outlets)):
            state_dict[str(outlets[i][0])+" "+str(outlets[i][2])+" "+str(outlets[i][3])] = states[i]
        
        return {'Status': state_dict}


class Outletcontrol(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('status', type=str, required=True,
                                    help='No status provided',
                                    location='json')
        super(Outletcontrol, self).__init__()

    def get(self, outletid):
        if g.user.username == 'root':
            outlet = outlet_details(outletid)
        else:
            role = check_outlet_permission(g.user.id,outletid)
            if role is False:
                return {'message': 'User does not have neccesary permission'}
            else:
                outlet = outlet_details(outletid)
        pdu = Pdu_obj(outlet[0],161,outlet[1])
        state = pdu.get_outlet_status(outlet[2],outlet[3])
            
        states = []
        if state == 'Error':
            states.append("unable to get data")
        else:
            states.append(state)

        state_dict = {}
        state_dict[str(outlet[0])+" "+str(outlet[2])+" "+str(outlet[3])] = states[0]
        
        return {'Status': state_dict}

    def post(self, outletid):
        args = self.reqparse.parse_args()

        status = args['status']
        if g.user.username == 'root':
            outlet = outlet_details(outletid)
        else:
            role = check_outlet_permission(g.user.id,outletid)
            if role is False:
                return {'message': 'User does not have neccesary permission'}
            else:
                outlet = outlet_details(outletid)

        pdu = Pdu_obj(outlet[0],161,outlet[1])
        states = []
        ret_value = pdu.change_state(outlet[2],outlet[3],status)
        if 'No SNMP response received' in str(ret_value):
            states.append("unable to connect to pdu")
        else:
            states.append("chnaged state")
        state_dict = {}
        state_dict[str(outlet[0])+" "+str(outlet[2])+" "+str(outlet[3])] = states[0]
        
        return {'Status': state_dict}
