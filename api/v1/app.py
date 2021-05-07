#!/usr/bin/python3
"""API for the Airbnb clone"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from os import getenv
from models import storage
import os
app = Flask(__name__)
app.register_blueprint(app_views)
HBNB_API_HOST = getenv('HBNB_API_HOST')
if HBNB_API_HOST is None:
    HBNB_API_HOST = "0.0.0.0"
HBNB_API_PORT = getenv('HBNB_API_PORT')
if HBNB_API_PORT is None:
    HBNB_API_PORT = "5000"


@app.teardown_appcontext
def teardown(self):
    """Calls storage.close()"""
    storage.close()

if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
