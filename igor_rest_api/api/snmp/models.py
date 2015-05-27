from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from werkzeug import generate_password_hash, check_password_hash

from igor_rest_api import app
from igor_rest_api.db import db
from igor_rest_api.api.models import snmp_users 


class Snmpuser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique=True)
    pwdhash = db.Column(db.String(54))
    pdus = db.relationship('Pdu', secondary=snmp_users,
                            backref=db.backref('pdus',lazy='dynamic'))

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
        return Snmpuser.query.get(data['id'])


def create_snmp_root_user():
    # Create root user
    with app.app_context():
        root_user = Snmpuser.query.filter_by(username=app.config['ROOT_USER']).first()
        if not root_user:
            root_user = Snmpuser(app.config['ROOT_USER'], app.config['ROOT_PASS'])
            db.session.add(root_user)
            db.session.commit()
