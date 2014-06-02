#!/usr/bin/env python

# Database 
DB_NAME = 'development'
DB_USER = 'igor'
DB_PASS = 'igor'
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASS + '@localhost/' + DB_NAME

# Sessions
SECRET_KEY = 'secret'
