from flask import Flask

app = Flask(__name__)

# Configuration
app.secret_key = 'secret'

import api.routes
