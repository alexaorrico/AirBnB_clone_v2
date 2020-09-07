#!/usr/bin/python3
"""
API for AirBnB_clone_v3
"""

import os
from flask import Flask, jsonify, Response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app = Flask(__name__)



@app.teardown_appcontext
def teardown(self):
    """ handles teardown """
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
