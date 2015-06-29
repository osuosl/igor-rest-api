from igor_rest_api.api.models import snmp_users
from igor_rest_api.db import db


class Pdu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100), unique=True)
    ip = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(54))
    users = db.relationship('Snmpuser', secondary=snmp_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, hostname, ip, password):
        self.hostname = hostname
        self.ip = ip
        self.password = password
