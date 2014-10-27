from flask.ext.script import Manager

from . import app
from .config import ROOT_USER, ROOT_PASS
from .api import models

manager = Manager(app)

@manager.command
def init_db():
    print "Creating database schema..."
    models.init_db(app)
    print "Done"

def run():
    manager.run()
