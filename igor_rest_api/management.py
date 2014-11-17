from flask.ext.script import Manager

from igor_rest_api.api.models import db
from igor_rest_api.api.auth.models import create_root_user

manager = Manager()

@manager.command
def init_db():
    print "Creating database schema..."
    db.create_all()
    print "Creating root user"
    create_root_user()
    print "Done"

def run():
    manager.run()
