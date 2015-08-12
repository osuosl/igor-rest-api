#!/usr/bin/env python

from flask import url_for, g
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from igor_rest_api.api.grouping.login import rootauth
from igor_rest_api.api.constants import *
from igor_rest_api.api.grouping.models import (
        Group, Pdudetails, Outlets,
        Groupoutlets, Userpdus,
        Useroutletsgroups, Userdetails)
from igor_rest_api.api.grouping.utils import (
        query_group, pduipfromid,
        query_group_outlets)
from igor_rest_api.db import db


"""
    GET     /pdu       Returns the list of all the pdus and ther ids
    POST    /pdu       {'ip': pdu_ip_address,
                        'access_string': pdu_access_string }  Creates a new pdu entry in database
"""


class PdudetailsAPI(Resource):
    decorators = [rootauth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ip', type=str, required=True,
                                   help='No ip provided',
                                   location='json')
        self.reqparse.add_argument('fqdn', type=str, required=True,
                                   help='No fqdn provided',
                                   location='json')
        self.reqparse.add_argument('access_string', type=str, required=True,
                                   help='No access_string provided',
                                   location='json')
        super(PdudetailsAPI, self).__init__()

    def get(self):
        pdus = Pdudetails.query.all()
        return {'pdus': [{'id': pdu.id,
                          'ip': pdu.ip,
                          'fqdn' : pdu.fqdn}
                         for pdu in pdus]}

    def post(self):
        args = self.reqparse.parse_args()

        ip = args['ip']
        access_string = args['access_string']
        fqdn = args['fqdn']
        if Pdudetails.query.filter_by(ip=ip).first() is not None:
            return {'message': 'Pdu %s exists' % ip}, BAD_REQUEST
        else:
            pdu = Pdudetails(ip, fqdn, access_string)
            db.session.add(pdu)
            try:
                db.session.commit()
                return {'pdu_ip': pdu.ip,
                        'pdu_id': pdu.id,
                        'pdu_fqdn': pdu.fqdn,
                        'location': url_for('groupings_pdu', ip=pdu.ip,
                                            _external=True)}, CREATED
            except IntegrityError as e:
                return {'Error': 'Integrity Error'}


"""
    GET      /pdu/<string:ip>        Returns the details of pdu with specified ip address
    PUT      /pdu/<string:ip>        {'access_string': new_access_string }
                                Will update the access_string of pdu with speciifed ip address
    DELETE   /pdu/<string:ip>       Deletes the pdu from database
"""


class PdudetailAPI(Resource):
    decorators = [rootauth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('access_string', type=str, required=False,
                                   help='No access_string provided',
                                   location='json')
        self.reqparse.add_argument('ip', type=str, required=False,
                                   help='No ip provided',
                                   location='json')
        super(PdudetailAPI, self).__init__()

    def get(self, ip):
        pdu = Pdudetails.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        users = Userpdus.query.filter_by(pduid=pdu.id).all()
        userids = [ user.userid for user in users]
        usernames = []
        for userid in userids:
            usernames.append(Userdetails.query.filter_by(id=userid).first().username)
        return {'Pdudetails': [{'id': pdu.id,
                                'users': usernames,
                                'fqdn': pdu.fqdn,
                                'ip': pdu.ip}]}

    def delete(self, ip):
        pdu = Pdudetails.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        else:
            # delete outlets associatied with pdu
            outlets = Outlets.query.filter_by(pdu_id=pdu.id).all()
            for outlet in outlets:
                # delete groups associatied with outlets
                groupoutlets = Groupoutlets.query.filter_by(outlet_id=outlet.id).all()
                for groupoutlet in groupoutlets:
                    db.session.delete(groupoutlet)
                    db.session.commit()
                db.session.delete(outlet)
                db.session.commit()
            #delete users associatied with pdu
            userpdus = Userpdus.query.filter_by(pduid=pdu.id).all()
            for userpdu in userpdus:
                db.session.delete(userpdu)
                db.session.commit()
            db.session.delete(pdu)
            db.session.commit()
            return {'message': 'Pdu %s deleted' % pdu.ip}

    def put(self, ip):
        args = self.reqparse.parse_args()
        pdu = Pdudetails.query.filter_by(ip=ip).first()

        access_string = args['access_string']
        ip = args['ip']
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        else:
            if not access_string is None:
                pdu.access_string = access_string
            if not ip is None :
                pdu.ip = ip 
            db.session.add(pdu)
            db.session.commit()
            return {'message': 'Updated entry for pdu %s' % pdu.ip}


"""
    GET     /outlets                Returns the details of all the outlets
    POST    /outlets                {'pduid': pduid, 'towername': towername, 'outlet': outlet } 
                                    Creates a new outlet entry in database
"""


class PduoutletsAPI(Resource):
    decorators = [rootauth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pduid', type=str, required=True,
                                   help='No pdu id provided',
                                   location='json')
        self.reqparse.add_argument('towername', type=str, required=True,
                                   help='No towername provided',
                                   location='json')
        self.reqparse.add_argument('outlet', type=int, required=True,
                                   help='No outlet provided',
                                   location='json')
        super(PduoutletsAPI, self).__init__()

    def get(self):
        outlets = Outlets.query.all()
        return {'outlets': [{'pdu_ip': pduipfromid(outlet.pdu_id),
                             'id': outlet.id,
                             'tower': outlet.towername,
                             'outlet': outlet.outlet}
                            for outlet in outlets]}

    def post(self):
        args = self.reqparse.parse_args()

        pdu_id = args['pduid']
        towername = args['towername']
        outlet = args['outlet']
        outlet = Outlets(pdu_id, towername, outlet)
        db.session.add(outlet)
        db.session.commit()
        return {'outlet_id': outlet.id,
                'outlet_ip': pduipfromid(outlet.pdu_id),
                'location': url_for('groupings_outlet', id=outlet.id,
                                     _external=True)}, CREATED


"""
    GET     /outlets/<int:id>      Returns the details of outlet with specified id
    POST    /outlets/<int:id>   {'pduid': pduid,
                            'towername': towername, 'outlet': outlet }  Will update the details of outlet
    DELETE  /outlets/<int:id>      Deletes the outlet from database
"""


class PduoutletAPI(Resource):
    decorators = [rootauth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pduid', type=str,
                                   help='No pdu id provided',
                                   location='json')
        self.reqparse.add_argument('towername', type=str,
                                   help='No towername provided',
                                   location='json')
        self.reqparse.add_argument('outlet', type=int,
                                   help='No outlet provided',
                                   location='json')
        super(PduoutletAPI, self).__init__()

    def get(self, id):
        outlet = Outlets.query.filter_by(id=id).first()
        if not outlet:
            return {'message': 'outlet with id %s does not exist' % id},\
                    NOT_FOUND
        return {'outlet': [{'pdu_ip': pduipfromid(outlet.pdu_id),
                             'id': outlet.id,
                             'tower': outlet.towername,
                             'outlet': outlet.outlet}]}

    def delete(self, id):
        outlet = Outlets.query.filter_by(id=id).first()
        if not outlet:
            return {'message': 'outlet with id %s does not exist' % id},\
                    NOT_FOUND
        else:
            # delete the groups associatied with groups
            groupoutlets = Groupoutlets.query.filter_by(outlet_id=outlet.id).all()
            for groupoutlet in groupoutlets:
                db.session.delete(groupoutlet)
                db.session.commit()
            db.session.delete(outlet)
            db.session.commit()
            return {'message': 'outlet with id %s deleted' % outlet.id}

    def post(self, id):
        args = self.reqparse.parse_args()
        outlet = Outlets.query.filter_by(id=id).first()

        pduid = args['pduid'] if 'pduid' in args else None
        towername = args['towername'] if 'towername' in args else None
        outletnum = args['outlet'] if 'outlet' in args else None

        if not outlet:
            return {'message': 'outlet with id %s does not exist' % id}, NOT_FOUND
        else:
            if pduid:
                outlet.pdu_id = pduid
            if towername:
                outlet.towername = towername
            if outletnum:
                outlet.outlet = outletnum
            db.session.add(outlet)
            db.session.commit()
            return {'message': 'Updated entry for outlet %s' % outlet.id}


"""
    GET     /outlet_groups/groups         Returns the details of all the outletgroupings
    POST    /outlet_groups/groups {'name': groupingname }  Creates a outletgrouping with the specified name
"""


class GroupsAPI(Resource):
    decorators = [rootauth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No grouping name provided',
                                   location='json')
        super(GroupsAPI, self).__init__()

    def get(self):
        groups = Group.query.all()
        return {'groups': [{'id': group.id,
                            'name': group.name}
                           for group in groups]}

    def post(self):
        args = self.reqparse.parse_args()

        name = args['name']
        group = Group.query.filter_by(name=name).first()
        if group is not None:
            return {'message': 'Group %s already exists' % name}, BAD_REQUEST
        group = Group(name)
        db.session.add(group)
        db.session.commit()
        return {'group_id': group.id,
                'group_name': name,
                'location': url_for('groupings_group', groupid=group.id,
                                     _external=True)}, CREATED


"""
    GET     /outlet_groups/<int:id>       Returns the details of groupname and outlets belonging to outletgrouping
    PUT     /outlet_groups/<int:id>  {'name': new_group_name }   Updates the name of outletgrouping
    DELETE  /outlet_groups/<int:id>       Deletes the outletgrouping from database
"""


class GroupAPI(Resource):
    decorators = [rootauth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No grouping name provided',
                                   location='json')
        super(GroupAPI, self).__init__()

    def get(self, groupid):
        group = Group.query.filter_by(id=groupid).first()
        if not group:
            return {'message': 'group with id %s does not exist' % groupid}, NOT_FOUND
        outlets = query_group_outlets(groupid)
        users = Useroutletsgroups.query.filter_by(outletgroupid=groupid).all()
        userids = [ user.userid for user in users]
        usernames = []
        for userid in userids:
            usernames.append(Userdetails.query.filter_by(id=userid).first().username)
        return {'group': [{'id': group.id,
                           'name': group.name,
                           'users': usernames,
                           'outlets': outlets}]}

    def post(self, groupid):
        args = self.reqparse.parse_args()
        name = args['name']
        group = Group.query.filter_by(id=groupid).first()
        if not group:
            return {'message': 'group with id %s does not exist' % groupid}, NOT_FOUND
        else:
            group.name = name
            db.session.add(group)
            db.session.commit()
            return {'message': 'Updated entry for group %s' % group.id}

    def delete(self, groupid):
        group = Group.query.filter_by(id=groupid).first()
        if not group:
            return {'message': 'group with id %s does not exist' % groupid}, NOT_FOUND
        else:
            groupoutlets = Groupoutlets.query.filter_by(group_id=groupid).all()
            for groupoutlet in groupoutlets:
                db.session.delete(groupoutlet)
                db.session.commit()
            db.session.delete(group)
            db.session.commit()
            return {'message': 'group %s deleted' % group.name}


"""

    POST    /outlet_groups/<int:groupid>/<int:outletid>   Creates association between group_id and outlet_id
    DELETE  /outlet_groups/<int:groupid>/<int:outletid>     Deletes the association between group_id and outlet_id

"""


class GroupoutletsAPI(Resource):
    decorators = [rootauth.login_required]


    def put(self, groupid, outletid):
        new = Groupoutlets(groupid, outletid)
        db.session.add(new)
        db.session.commit()
        return {'Success': 'added outlet to group'}

    def delete(self, groupid, outletid):
        groupoutlet = Groupoutlets.query.filter_by(outlet_id=outletid,
                                                   group_id=groupid).first()
        if not groupoutlet:
            return {'message': 'grouping doesn"t exist'}
        else:
            db.session.delete(groupoutlet)
            db.session.commit()
            return {'Success': 'deleted outlet from grouping'}

"""

    PUT    /pdu/<int:pduid>/<int:userid>   Creates association between pdu and user
    DELETE  /pdu/<int:pduid>/<int:userid>   Deletes the association between pdu and user

"""


class UserpdusAPI(Resource):
    decorators = [rootauth.login_required]


    def put(self, pduid, userid):
        check = Userpdus.query.filter_by(pduid=pduid,
                                         userid=userid).first()
        print check
        if not check:
            new = Userpdus(userid, pduid)
            db.session.add(new)
            db.session.commit()
            return {'Success': 'added user to pdu'}
        else:
            return {'Error': 'Relation already exists'}

    def delete(self, pduid, userid):
        relation = Userpdus.query.filter_by(pduid=pduid,
                                                   userid=userid).first()
        if not relation:
            return {'message': 'grouping doesn"t exist'}
        else:
            db.session.delete(relation)
            db.session.commit()
            return {'Success': 'deleted user from pdu'}
