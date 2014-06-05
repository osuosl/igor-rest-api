#!/usr/bin/env python

from flask import Flask
from config import ROOT_USER, ROOT_PASS
from flask.ext.script import Manager
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object('config')

from models import db, User
db.init_app(app)

# Create tables and root user
with app.app_context():
    db.create_all()
    root_user = User.query.filter_by(username=ROOT_USER).first()
    if not root_user:
        root_user = User(ROOT_USER, ROOT_PASS)
        db.session.add(root_user)
        db.session.commit()

manager = Manager(app)

import routes
