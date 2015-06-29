from igor_rest_api.api.pdus.models import Pdu


def check_permission(user, pdu_ip):
    pdu_dict = {}
    for pdu in user.pdus:
        pdu_dict[pdu.ip] = pdu.password
    if pdu_ip in pdu_dict.keys():
        return pdu_dict[pdu_ip]
    else:
        return False


def get_access_string(pdu_ip):
    pdu = Pdu.query.filter_by(ip=pdu_ip).first()
    if pdu is None:
        return False
    else:
        return pdu.password
