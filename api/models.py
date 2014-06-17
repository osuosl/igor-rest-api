from api import app
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

db = SQLAlchemy()

machine_users = db.Table('permissions',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('machine_id', db.Integer, db.ForeignKey('machine.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique=True)
    pwdhash = db.Column(db.String(54))
    machines = db.relationship('Machine', secondary=machine_users,
                               backref=db.backref('machines', lazy='dynamic'))
   
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
        return User.query.get(data['id'])

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hostname = db.Column(db.String(100), unique=True)
    fqdn = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(54))
    users = db.relationship('User', secondary=machine_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, hostname, fqdn, username, password):
        self.hostname = hostname
        self.fqdn = fqdn
        self.username = username
        self.password = password
