from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

machine_users = db.Table(
    'permissions',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('machine_id', db.Integer, db.ForeignKey('machine.id'))
)

