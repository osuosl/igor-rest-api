#!/usr/bin/env python

from flask import url_for
from flask.ext.restful import Resource

from igor_rest_api.api.snmp.login import auth
from igor_rest_api.api.snmp.models import Snmpuser
from igor_rest_api.api.constants import *
from igor_rest_api.db import db

from ..models import Pdu

# Pdu-user permissions endpoints
"""
    GET     /Snmpusers/:username/pdus   Returns the list of pdus 
                                        accessible by :username
"""
class UserPdusAPI(Resource):
    decorators = [auth.login_required]

    def get(self, username):
        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        return {'username': user.username,
                'pdus': [{'ip': pdu.ip,
                              'location': url_for('pdu',
                                                  ip=pdu.ip,
                                                  _external=True)}
                              for pdu in user.pdus]}
"""
    GET     /Snmpusers/:username/pdu/:ip     Returns 200 or 404,
                                                    depending on :username's
                                                    access to :ip
    PUT     /Snmpusers/:username/pdu/:ip     Adds :username-:ip
                                                    entry to the permissions
                                                    table
    DELETE  /Snmpusers/:username/pdu/:ip     Deletes
                                                    :username-:ip entry
                                                    in the permissions table
"""
class UserPduAPI(Resource):
    decorators = [auth.login_required]

    def get(self, username, ip):
        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Host %s does not exist' % ip}, NOT_FOUND

        if pdu in user.pdus:
            return {'username': username,
                    'ip': ip,
                    'location': url_for('pdu', ip=ip,
                                        _external=True)}
        else:
            return {'message': 'User %s does not have permission for pdu %s'
                    % (username, ip)}, NOT_FOUND

    def put(self, username, ip):
        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND

        print dir(user)
        if pdu not in user.pdus:
            user.pdus.append(pdu)
            db.session.add(user)
            db.session.commit()

        return {'message': 'Created permission for user %s to pdu %s'
                % (username, ip)}, CREATED

    def delete(self, username, ip):
        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND

        if pdu in user.pdus:
            user.pdus.remove(pdu)
            db.session.add(user)
            db.session.commit()

            return {'message': 'Deleted permission for user %s to pdu %s'
                    % (username, ip)}
        else:
            return {'message': 'User %s does not have permission for pdu %s'
                    % (username, ip)}, NOT_FOUND

"""
    GET     /pdu/:ip/users   Returns the list of users with access
                                        to :ip
"""
class PduUsersAPI(Resource):
    decorators = [auth.login_required]

    def get(self, ip):
        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND

        return {'ip': pdu.ip,
                'users': [{'username': user.username,
                           'location': url_for('snmpuser', username=user.username,
                                               _external=True)}
                            for user in pdu.users]}
"""
    GET     /pdu/:ip/users/:username     Returns 200 or 404,
                                                    depending on :username's
                                                    access to :ip
    PUT     /pdu/:ip/users/:username     Adds :username-:ip
                                                    entry to the permissions
                                                    table
    DELETE  /pdu/:ip/users/:username     Deletes
                                                    :username-:ip entry
                                                    in the permissions table
"""
class PduUserAPI(Resource):
    decorators = [auth.login_required]

    def get(self, ip, username):
        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND

        if user in pdu.users:
            return {'username': username,
                    'ip': ip,
                    'location': url_for('snmpuser', username=username,
                                        _external=True)}
        else:
            return {'message': 'User %s does not have permission for pdu %s'
                    % (username, ip)}, NOT_FOUND

    def put(self, ip, username):
        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND

        if user not in pdu.users:
            pdu.users.append(user)
            db.session.add(pdu)
            db.session.commit()

        return {'message': 'Created permission for user %s to pdu %s'
                % (username, ip)}, CREATED

    def delete(self, ip, username):
        user = Snmpuser.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User %s does not exist' % username}, NOT_FOUND

        pdu = Pdu.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND

        if user in pdu.users:
            pdu.users.remove(user)
            db.session.add(pdu)
            db.session.commit()

            return {'message': 'Deleted permission for user %s to pdu %s'
                    % (username, ip)}
        else:
            return {'message': 'User %s does not have permission for pdu %s'
                    % (username, ip)}, NOT_FOUND
