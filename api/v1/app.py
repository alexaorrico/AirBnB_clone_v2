#!/usr/bin/python3
"""
This module runs the flask api on
"""
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(e):
    """ handle page not found error """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(e):
    """ teardown """
    storage.close()


if __name__ == "__main__":
    app.run(getenv('HBNB_API_HOST'), getenv('HBNB_API_PORT'), threaded=True)
