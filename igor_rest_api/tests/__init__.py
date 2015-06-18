#!/usr/bin/env python

from flask.ext.testing import TestCase
from flask import Flask

from igor_rest_api import app
from igor_rest_api.db import db
from igor_rest_api.api.auth.models import create_root_user
from igor_rest_api.api.snmp.models import create_snmp_root_user
from igor_rest_api.api.grouping.models import create_grouping_root_user

class IgorApiTestCase(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['ROOT_USER'] = 'root'
        app.config['ROOT_PASS'] = 'root'
        app.config['SECRET_KEY'] = 'secret'
        self.app = app
        self.db = db
        return app

    def setUp(self):
        self.db.create_all()
        create_root_user()
        create_snmp_root_user()
        create_grouping_root_user()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
