from flask.ext.script import Manager

from . import app
from .api.auth.models import create_root_user
from .config import ROOT_USER, ROOT_PASS
from .db import db

manager = Manager(app)

@manager.command
def init_db():
    print "Creating database schema..."
    db.create_all()
    print "Creating root user"
    create_root_user()
    print "Done"

def run():
    manager.run()
