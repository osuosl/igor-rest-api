#!/usr/bin/env python

from flask import g, url_for, jsonify, request
from flask.ext.restful import Resource, reqparse

from igor_rest_api.api.constants import *
from igor_rest_api.db import db

from igor_rest_api.api.snmp.login import auth
from igor_rest_api.api.snmp.models import Snmpuser
from igor_rest_api.api.pdus.models import Pdu

from pudmaster import Pdu_obj
from utils import check_permission, get_access_string

# Pdu management endpoints
"""
    GET /pdu/:ip/status                Returns status of all towers
"""
class Pdustatus(Resource):
    decorators = [auth.login_required]

    def get(self,ip):

        if g.user.username != 'root':
            pdu_pass = check_permission(g.user,ip)
        else:
            pdu_pass = get_access_string(ip)

        if pdu_pass == False:
            return {'Error':'No access'}

        else:

            pdu = Pdu_obj(ip,161,pdu_pass)
            try:
                status, name = pdu.complete_status()
            except ValueError:
                return {'error': 'Unable to get data'}

            if status == "Error":
                return {'error': 'Unable to get data'}

            status_dict = {}
            for i in range(len(status)):
                status_dict[name[i]] = status[i]
            return {'status' : status_dict }

"""
    GET /pdu/:ip/:tower/:outlet Returns status of specified outlet 
"""
class OutletStatus(Resource):
    decorators = [auth.login_required]

    def get(self,ip,tower,outlet):

        if g.user.username != 'root':
            pdu_pass = check_permission(g.user,ip)
        else:
            pdu_pass = get_access_string(ip)

        if pdu_pass == False:
            return {'Error': 'No access'}

        else:
            pdu = Pdu_obj(ip,161,pdu_pass)
            state = pdu.get_outlet_status(tower,outlet)
            
            if state == 'Error':
                return {'Error': 'Unable to get data'}
            else:
                return {'state' : state}


    def post(self,ip,tower,outlet):

        json = request.json
        if g.user.username != 'root':
            pdu_pass = check_permission(g.user,ip)
        else:
            pdu_pass = get_access_string(ip)

        if pdu_pass == False:
            return {'Error': 'No access'}

        else:
            pdu = Pdu_obj(ip,161,pdu_pass)
            ret_value = pdu.change_state(tower,outlet,json['state'])
            if 'No SNMP response received' in str(ret_value):
                return { 'Error' : 'unable to connect to pdu' }
            else:
                return {'Success' : 'Changed state'}



