#!/usr/bin/env python

from flask import url_for, g
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from igor_rest_api.api.grouping.login import rootauth
from igor_rest_api.api.constants import *
from igor_rest_api.api.grouping.models import Group, Pdudetails, Outlets, Groupoutlets
from igor_rest_api.api.grouping.utils import query_group, pduipfromid, query_group_outlets
from igor_rest_api.db import db

"""
    GET     /outlet_groups/pdu           Returns the list of all the pdus and ther ids
    POST    /outlet_groups/pdu {'ip': pdu_ip_address,
                    'access_string': pdu_access_string }    Creates a new pdu entry in database
"""
class PdudetailsAPI(Resource):
    decorators = [rootauth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('ip', type=str, required=True,
                                    help='No ip provided',
                                    location='json')
        self.reqparse.add_argument('access_string', type=str, required=True,
                                    help='No access_string provided',
                                    location='json')
        super(PdudetailsAPI, self).__init__()

    def get(self):
        pdus = Pdudetails.query.all()
        return {'pdus': [{'id': pdu.id,
                            'ip': pdu.ip}
                              for pdu in pdus]}
   

    def post(self):
        args = self.reqparse.parse_args()

        ip = args['ip']
        access_string = args['access_string']
        if Pdudetails.query.filter_by(ip=ip).first() is not None:
            return {'message': 'Pdu %s exists' % ip}, BAD_REQUEST
        else:
            pdu = Pdudetails(ip, access_string)
            db.session.add(pdu)
            try:
                db.session.commit()
                return {'Success':'added pdu %s ' % ip}, CREATED
            except IntegrityError as e:
                return {'Error': 'Integrity Error'}


"""
    GET      /outlet_groups/pdu/<string:ip>                       Returns the details of pdu with specified ip address
    PUT      /outlet_groups/pdu/<string:ip> 
                      {'access_string': new_access_string }   Will update the access_string of pdu with speciifed ip address
    DELETE   /outlet_groups/pdu/<string:ip>                       Deletes the pdu from database
"""
class PdudetailAPI(Resource):
    decorators = [rootauth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('access_string', type=str, required=True,
                                    help='No access_string provided',
                                    location='json')
        super(PdudetailAPI, self).__init__()

    def get(self, ip):
        pdu = Pdudetails.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        return {'Pdudetails' : [{'id': pdu.id,
                                 'ip': pdu.ip}]}


    def delete(self, ip):
        pdu = Pdudetails.query.filter_by(ip=ip).first()
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        else:
            db.session.add(pdu)
            db.session.commit()
            db.session.delete(pdu)
            db.session.commit()
            return {'message': 'Pdu %s deleted' % pdu.ip}

    def put(self, ip):
        args = self.reqparse.parse_args()
        pdu = Pdudetails.query.filter_by(ip=ip).first()

        access_string = args['access_string']
        if not pdu:
            return {'message': 'Pdu %s does not exist' % ip}, NOT_FOUND
        else:
            pdu.access_string = access_string
            db.session.add(pdu)
            db.session.commit()
            return {'message': 'Updated entry for pdu %s' % pdu.ip}


"""
    GET     /outlet_groups/outlets                                      Returns the details of all the outlets 
    POST    /outlet_groups/outlets    {'pduid': pduid,
                        'towername': towername, 'outlet': outlet }  Creates a new outlet entry in database
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
        outlet = Outlets(pdu_id,towername,outlet)
        db.session.add(outlet)
        db.session.commit()
        return {'Success': 'added outlet'}, CREATED


"""
    GET     /outlet_groups/outlets/<int:id>                                 Returns the details of outlet with specified id
    PUT     /outlet_groups/outlets/<int:id>   {'pduid': pduid,
                            'towername': towername, 'outlet': outlet }  Will update the details of outlet 
    DELETE  /outlet_groups/outlets/<int:id>                                 Deletes the outlet from database
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
            return {'message': 'outlet with id %s does not exist' % id}, NOT_FOUND
        return {'outlets' : [{'pdu_ip': pduipfromid(outlet.pdu_id),
                              'id': outlet.id,
                              'tower': outlet.towername,
                              'outlet': outlet.outlet}]}

    def delete(self, id):
        outlet = Outlets.query.filter_by(id=id).first()
        if not outlet:
            return {'message': 'outlet with id %s does not exist' % id}, NOT_FOUND
        else:
            db.session.add(outlet)
            db.session.commit()
            db.session.delete(outlet)
            db.session.commit()
            return {'message': 'outlet with id %s deleted' % outlet.id}

    def put(self, id):
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
    GET     /outlet_groups/groups                               Returns the details of all the outletgroupings
    POST    /outlet_groups/groups {'name': groupingname }       Creates a outletgrouping with the specified name
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
                            'name': group.name }
                            for group in groups]}


    def post(self):
        args = self.reqparse.parse_args()

        name = args['name']
        group = Group.query.filter_by(name=name).first()
        if group is not None:
            return {'message' : 'Group %s already exists' %name}, BAD_REQUEST
        group = Group(name)
        db.session.add(group)
        db.session.commit()
        return {'Success' : 'added group %s' %name}, CREATED


"""
    GET     /outlet_groups/groups/<int:id>                              Returns the details of groupname and outlets belonging to outletgrouping 
    PUT     /outlet_groups/groups/<int:id>  {'name': new_group_name }   Updates the name of outletgrouping
    DELETE  /outlet_groups/groups/<int:id>                              Deletes the outletgrouping from database
"""
class GroupAPI(Resource):
    decorators = [rootauth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, 
                                    help='No grouping name provided',
                                    location='json')
        super(GroupAPI, self).__init__()
        
    def get(self, id):
       group = Group.query.filter_by(id=id).first()
       if not group:
            return {'message': 'group with id %s does not exist' % id}, NOT_FOUND
       outlets = query_group_outlets(id)
       return {'group': [{'id': group.id,
                          'name': group.name,
                          'outlets': outlets}]}

    def put(self, id):
       args = self.reqparse.parse_args()
       name = args['name']
       group = Group.query.filter_by(id=id).first()
       if not group:
            return {'message': 'group with id %s does not exist' % id}, NOT_FOUND
       else:
            group.name = name
            db.session.add(group)
            db.session.commit()
            return {'message': 'Updated entry for group %s' % group.id}

    def delete(self, id):
       group = Group.query.filter_by(id=id).first()
       if not group:
            return {'message': 'group with id %s does not exist' % id}, NOT_FOUND
       else:
            db.session.delete(group)
            db.session.commit()
            return {'message': 'group %s deleted' % group.name}


"""
    GET     /outlet_groups/groupings                        Returns the associations between outletgroupings and outlets
    POST    /outlet_groups/groupings {'outlet_id': outlet_id,
                            'group_id': group_id }      Creates association between group_id and outlet_id
    DELETE  /outlet_groups/groupings {'outlet_id': outlet_id,
                            'group_id': group_id }      Deletes the association between group_id and outlet_id
"""
class GroupoutletsAPI(Resource):
    decorators = [rootauth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('outlet_id', type=int, required=True,
                                    help='No outlet id was provided',
                                    location='json')

        self.reqparse.add_argument('group_id', type=int, required=True,
                                    help='No grouping id was provided',
                                    location='json')

    def get(self):
        groupoutlets = Groupoutlets.query.all()
        return {'groupoutlets': [{'group_id': groupoutlet.group_id,
                                  'outlet_id': groupoutlet.outlet_id}
                                  for groupoutlet in groupoutlets]}

    def post(self):
        args = self.reqparse.parse_args()
        outlet_id = args['outlet_id']
        group_id = args['group_id']
        new = Groupoutlets(group_id, outlet_id)
        db.session.add(new)
        db.session.commit()
        return {'Success' : 'added outlet to group'}

    def delete(self):
        args = self.reqparse.parse_args()
        outlet_id = args['outlet_id']
        group_id = args['group_id']
        groupoutlet = Groupoutlets.query.filter_by(outlet_id=outlet_id,group_id=group_id).first()
        if not groupoutlet:
            return {'message': 'grouping doesn"t exist'}
        else:
            db.session.delete(groupoutlet)
            db.session.commit()
            return {'Success': 'deleted grouping'}
