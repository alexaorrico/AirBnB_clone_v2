#!/usr/bin/python3
"""
Module app
"""
from flask import Flask, Blueprint, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ closes the session """
    storage.close()


if __name__ == "__main__":

    host_env = getenv("HBNB_API_HOST", "0.0.0.0")
    port_env = getenv("HBNB_API_PORT", "5000")
    app.run(host=host_env, port=port_env)
