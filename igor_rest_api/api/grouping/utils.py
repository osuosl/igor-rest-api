#!/usr/bin/env python
#This file useful utilites which can be used in views

from igor_rest_api.api.grouping.models import Group, Pdudetails, Outlets, Groupoutlets, \
                                                Userdetails, Useroutletsgroups

def query_group(id):
    #takes groupid as input and returns the details 
    #of outlets belonging to outletgrouping
        outletids = []
        temp = Groupoutlets.query.filter_by(group_id=id).all()
        for i in temp:
            outletids.append(i.outlet_id)

        pdus = []
        for i in outletids:
            temp = Outlets.query.filter_by(id=i).all()
            for j in temp:
                temp_pdu = query_pdudetails(j.pdu_id)
                temp_pdu.extend([j.towername,j.outlet])
                pdus.append(temp_pdu)
        return pdus


def query_group_outlets(id):
    #this function is similar to query_group except this
    #will not return the access_string of pdus belonging to outletgrouping
        outletids = []
        temp = Groupoutlets.query.filter_by(group_id=id).all()
        for i in temp:
            outletids.append(i.outlet_id)

        pdus = []
        for i in outletids:
            temp = Outlets.query.filter_by(id=i).all()
            for j in temp:
                temp_pdu = query_pduip(j.pdu_id)
                temp_pdu.extend([j.towername,j.outlet])
                pdus.append(temp_pdu)
        return pdus


def query_pdudetails(id):
    #this function will take pdu_id as input 
    #and returns the pdu_ip and access_string 
    pdu = Pdudetails.query.filter_by(id=id).first()
    retvalue = []
    retvalue.append(pdu.ip)
    retvalue.append(pdu.access_string)
    return retvalue


def pduipfromid(id):
    pdu = Pdudetails.query.filter_by(id=id).first()
    if pdu is None:
        return 'invaild ip'
    return pdu.ip


def query_pduip(id):
    pdu = Pdudetails.query.filter_by(id=id).first()
    retvalue = []
    retvalue.append(pdu.ip)
    return retvalue


def get_user_id(username):
    user = Userdetails.query.filter_by(username=username).first()
    return user.id


def outlet_details(id):
    temp = Outlets.query.filter_by(id=id).all()
    for j in temp:
        temp_pdu = query_pdudetails(j.pdu_id)
        temp_pdu.extend([j.towername,j.outlet])
    return temp_pdu


def check_outlet_permission(userid,outletid):
    #this function will validate whether a user has permission to control a outlet
    usergroups = Useroutletsgroups.query.filter_by(userid=userid).all()

    for group in usergroups:
        if Groupoutlets.query.filter_by(group_id=group.outletgroupid,outlet_id=outletid).first() is not None:
            return True
    return False
