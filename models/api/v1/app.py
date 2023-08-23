#!/usr/bin/python3
""" flusk app """

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)

if __name__ == "__main__":
    app.run(host = getenv('HBNB_API_HOST') or '0.0.0.0', port = getenv('HBNB_API_PORT') or 5000, threaded=True)