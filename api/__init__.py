#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)
app.config.from_object('api.config')

from models import db
db.init_app(app)

import api.routes
