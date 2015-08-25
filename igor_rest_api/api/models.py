from igor_rest_api import db

machine_users = db.Table('permissions',
                         db.Column('user_id', db.Integer,
                                   db.ForeignKey('user.id')),
                         db.Column('machine_id', db.Integer,
                                   db.ForeignKey('machine.id')))
