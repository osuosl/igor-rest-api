from flask import Flask
from flask.ext.restful import Api

from .db import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    app.config.from_object('igor_rest_api.config')
    return app


app = create_app()

from .api import routes
igor_api = Api(app)
routes.setup(igor_api)

