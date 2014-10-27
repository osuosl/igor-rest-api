from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object('igor_rest_api.config')

from .api import routes
routes.setup(app)

