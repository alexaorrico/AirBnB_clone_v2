#!/usr/bin/python3
"""
Module app
"""
from flask import Flask, Blueprint, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """ closes the session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """note that we set the 404 status explicitly"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":

    host_env = getenv("HBNB_API_HOST", "0.0.0.0")
    port_env = getenv("HBNB_API_PORT", "5000")
    app.run(host=host_env, port=port_env)
