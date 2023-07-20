#!/usr/bin/python3
""" returns status of API """

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """ exits storage by calling close """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    hosts = getenv('HBNB_API_HOST', default='0.0.0.0')
    ports = getenv('HBNB_API_PORT', default=5000)
    app.run(host=hosts, port=ports, threaded=True)
