from igor_rest_api.api.models import db, machine_users

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    def __eq__(self, machine):
        return self.hostname == machine.hostname
