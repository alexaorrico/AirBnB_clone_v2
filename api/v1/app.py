#!/usr/bin/python3
""" flask app main file """
from flask import Flask
from os import environ
from api.v1.views import app_views

HBNB_API_PORT = environ.get("HBNB_API_PORT")
HBNB_API_HOST = environ.get("HBNB_API_HOST")

app = Flask(__name__)
app.register_blueprint(app_views)

if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
