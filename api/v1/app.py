#!/usr/bin/python3
""" Flask App """

from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


if __name__ == "__main__":
    app.run(host=)
