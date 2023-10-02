#!/usr/bin/python3
"""Status API"""

from flask import Flask, Blueprint
from flask_cors import CORS
from models import storage
from flask import jsonify
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {'origins': ['0.0.0.0']}})


@app.teardown_appcontext
def close_s(x=None):
    """Close session at the end"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
