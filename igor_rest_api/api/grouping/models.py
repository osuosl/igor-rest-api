from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from werkzeug import generate_password_hash, check_password_hash

from igor_rest_api import app
from igor_rest_api.db import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


class Pdudetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(70), unique=True)
    fqdn = db.Column(db.String(70), unique=True)
    access_string = db.Column(db.String(70))

    def __init__(self, ip, fqdn, access_string):
        self.ip = ip
        self.fqdn = fqdn
        self.access_string = access_string


class Outlets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pdu_id = db.Column(db.Integer, db.ForeignKey('pdudetails.id'))
    towername = db.Column(db.String(2))
    outlet = db.Column(db.Integer)

    def __init__(self, pdu_id, towername, outlet):
        self.pdu_id = pdu_id
        self.towername = towername
        self.outlet = outlet


class Groupoutlets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlets.id'))

    def __init__(self, group_id, outlet_id):
        self.group_id = group_id
        self.outlet_id = outlet_id


class Userdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def validate_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return Userdetails.query.get(data['id'])


class Useroutletsgroups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('userdetails.id'))
    outletgroupid = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __init__(self, userid, outletgroupid):
        self.userid = userid
        self.outletgroupid = outletgroupid

class UserPdus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('Userdetails.id'))
    pduid = db.Column(db.Integer, db.ForeignKey('Pdudetails.id'))

    def __init__(self, userid, pduid):
        self.userid = userid
        self.pduid = pduid

def create_grouping_root_user():
    # Create root user
    with app.app_context():
        root_user = Userdetails.query.filter_by(username=app.config['ROOT_USER']).first()
        if not root_user:
            root_user = Userdetails(app.config['ROOT_USER'],
                                    app.config['ROOT_PASS'])
            db.session.add(root_user)
            db.session.commit()
