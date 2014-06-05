#!/usr/bin/env python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
ROOT_USER = 'root'
ROOT_PASS = 'root'
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'app.db')

# Sessions
SECRET_KEY = 'secret'

# Development
DEBUG = True
