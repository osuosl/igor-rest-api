from flask import current_app
from flask.ext import script
from flask.ext.script.commands import InvalidCommand

from igor_rest_api import create_app
from igor_rest_api.api.auth.models import User
from igor_rest_api.api.models import db

manager = script.Manager(create_app)
db_manager = script.Manager(usage="Perform database operations")

manager.add_command("database", db_manager)

@db_manager.command
def create():
    """
    Creates database tables from sqlalchemy models
    """
    print "Creating database schema..."
    db.create_all()
    print "Done"

@db_manager.command
def drop():
    """
    Drops all database tables
    """
    if script.prompt_bool("Are you sure you want to delete all your database tables?"):
        db.drop_all()
        print "Dropped tables"

@db_manager.command
def create_user(username=None):
    """
    Creates a username with the specified username, and prompts for a password.
    """
    if not username:
        username = script.prompt("Enter your username")

    u = User.query.filter_by(username=username).first()
    if u:
        raise InvalidCommand("User '%s' already exists!" % username)

    pw = script.prompt_pass("Enter your password")

    u = User(username=username, password=pw)

    db.session.add(u)
    db.session.commit()
    print "Successfully created user '%s'" % username
