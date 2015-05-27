#!/usr/bin/env python

from flask import url_for
from flask.ext.restful import Resource, reqparse

from igor_rest_api.api.snmp.login import auth
from igor_rest_api.api.constants import *
from igor_rest_api.api.pdus.models import Pdu 
from igor_rest_api.db import db



# Pdu  management endpoints
"""
    GET     /pdus                           Returns the list of pdus
    POST    /pdus {'hostname': hostname,
                       'username': username,
                       'ip':     ip,
                       'password': password}    Creates a new pdu entry
"""
class PdusAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hostname', type=str, required=True,
                                    help='No hostname provided',
                                    location='json')
        self.reqparse.add_argument('ip', type=str, required=True,
                                    help='No ip provided',
                                    location='json')
        self.reqparse.add_argument('username', type=str, required=True,
                                    help='No username provided',
                                    location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                    help='No password provided',
                                    location='json')
        super(PdusAPI, self).__init__()

   

    def get(self):
        pdus = []
        for pdu in Pdu.query.all():
            pdus.append(pdu.ip)
        return {'pdus': [{'ip': ip,
                              'users': url_for('pdu_users',
                                               ip=ip,
                                               _external=True),
                              'location': url_for('pdu',
                                                  ip=ip,
                                                  _external=True)}
                              for ip in pdus]}


    def post(self):
        args = self.reqparse.parse_args()

        hostname = args['hostname']
        ip = args['ip']
        username = args['username']
        password = args['password']
        if Pdu.query.filter_by(ip=ip).first() is not None:
            return {'message': 'Host %s exists' % hostname}, BAD_REQUEST
        else:
            pdu = Pdu(hostname, ip, username, password)
            db.session.add(pdu)
            db.session.commit()
            return {'ip': pdu.ip,
                    'users': url_for('pdu_users', ip=ip,
                                     _external=True),
                    'location': url_for('pdu', ip=pdu.ip,
                                        _external=True)}, CREATED

 

"""
    GET     /pdus/:ip             Return details for the machine
    DELETE  /pdus/:ip             Delete the machine
    PUT     /pdus/:ip             Update ip/username/password
"""
class PduAPI(Resource):
    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ip', type=str,
                                    help='No ip provided', location='json')
        self.reqparse.add_argument('username', type=str,
                                    help='No username provided',
                                    location='json')
        self.reqparse.add_argument('password', type=str,
                                    help='No password provided',
                                    location='json')
        super(PduAPI, self).__init__()

    def get(self, ip):
        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        else:
            return {'hostname': pdu.hostname,
                    'ip': pdu.ip,
                    'users': url_for('pdu_users', ip=ip,
                                     _external=True),
                    'location': url_for('pdu', ip=ip,
                                        _external=True)}
                    

    def delete(self, ip):
        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        else:
            pdu.users = []
            db.session.add(pdu)
            db.session.commit()
            db.session.delete(pdu)
            db.session.commit()
            return {'message': 'Pdu %s deleted' % pdu.ip}

    def put(self, ip):
        args = self.reqparse.parse_args()
        pdu = Pdu.query.filter_by(ip=ip).first()

        hostname = args['hostname'] if 'hostname' in args else None
        username = args['username'] if 'username' in args else None
        password = args['password'] if 'password' in args else None

        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        else:
            if hostname:
                pdu.hostname = hostname 
            if username:
                pdu.username = username
            if password:
                pdu.password = password
            db.session.add(pdu)
            db.session.commit()
            return {'message': 'Updated entry for pdu %s' % pdu}
