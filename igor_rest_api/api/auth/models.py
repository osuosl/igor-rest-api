from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from werkzeug import generate_password_hash, check_password_hash

from igor_rest_api.api.models import db, machine_users


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
        s = Serializer(current_app.config.get('SECRET_KEY'), expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def validate_auth_token(token):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(data['id'])

    def __eq__(self, user):
        return self.username == user.username

def create_root_user():
    # Create root user
    with current_app.app_context():
        root_user = User.query.filter_by(username=current_app.config.get('ROOT_USER')).first()
        if not root_user:
            root_user = User(current_app.config.get('ROOT_USER'), current_app.config.get('ROOT_PASS'))
            db.session.add(root_user)
            db.session.commit()