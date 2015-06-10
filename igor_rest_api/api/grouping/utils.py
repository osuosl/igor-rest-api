#!/usr/bin/env python

from igor_rest_api.api.grouping.models import Group, Pdudetails, Outlets, Groupoutlets

def query_group(id):
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


def query_pdudetails(id):
    pdu = Pdudetails.query.filter_by(id=id).first()
    retvalue = []
    retvalue.append(pdu.ip)
    retvalue.append(pdu.access_string)
    return retvalue


def pduipfromid(id):
    pdu = Pdudetails.query.filter_by(id=id).first()
    return pdu.ip
