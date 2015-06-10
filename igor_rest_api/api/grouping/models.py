from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from werkzeug import generate_password_hash, check_password_hash

from igor_rest_api import app
from igor_rest_api.db import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)

    def __init__(self, name):
        self.name = name


class Pdudetails(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ip = db.Column(db.String(70), unique = True)
    access_string = db.Column(db.String(70))

    def __init__(self, ip, access_string):
        self.ip = ip
        self.access_string = access_string


class Outlets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pdu_id = db.Column(db.Integer, db.ForeignKey('pdudetails.id'))
    towername = db.Column(db.String(2))
    outlet = db.Column(db.Integer)

    def __init__(self, pdu_id, towername, outlet):
        self.pdu_id = pdu_id
        self.towername = towername
        self.outlet = outlet


class Groupoutlets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlets.id'))

    def __init__(self,group_id,outlet_id):
        self.group_id = group_id
        self.outlet_id = outlet_id
