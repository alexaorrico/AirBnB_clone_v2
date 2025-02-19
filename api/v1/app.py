#!/usr/bin/python3
""" a basic flask application """

import sys
import os

from flask import Flask, jsonify
from flask_cors import CORS
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handel error message """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
