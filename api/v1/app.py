#!/usr/bin/python3
""" Flask App """

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)


if __name__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST")
    HBNB_API_PORT = getenv("HBNB_API_PORT")
    if HBNB_API_HOST is None:
        HBNB_API_HOST = "0.0.0.0"
    if HBNB_API_PORT is None:
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
