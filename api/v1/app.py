#!/usr/bin/python3
"""
Module app
"""

from api.v1.views import app_views
from flasgger import Swagger
from flask import (Blueprint, Flask, jsonify, make_response)
from flask_cors import (CORS, cross_origin)
from models import storage
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext()
def teardown_db(self):
    """teardown db"""
    storage.close()


@app.errorhandler(404)
def err404(error):
    """404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(
        host=environ.getenv(
            'HBNB_API_HOST',
            '0.0.0.0'),
        port=environ.getenv(
            'HBNB_API_PORT',
            '5000'),
        threaded=True)
