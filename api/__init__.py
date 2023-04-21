#!/usr/bin/python3
"""Initialization for the RESTful API"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
