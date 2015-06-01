def check_permission(user,pdu_ip):
    pdu_dict = {}
    for pdu in user.pdus:
        pdu_dict[pdu.ip] = pdu.password
    if pdu_ip in pdu_dict.keys():
        return pdu_dict[pdu_ip]
    else:
        return False
