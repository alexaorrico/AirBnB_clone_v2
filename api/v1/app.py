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


@app.teardown_appcontext
def teardown(self):
    """ handles teardown """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ handles 404 errors """
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == '__main__':
    try:
        host = os.environ.get('HBNB_API_HOST')
    except:
        host = '0.0.0.0'

    try:
        port = os.environ.get('HBNB_API_PORT')
    except:
        port = '5000'

    app.run(host=host, port=port)
