#!/usr/bin/python3
"""
Module: app
"""
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """ close storage session """
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    """ returns the 404 request error in JSON format """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    _host = getenv('HBNB_API_HOST', '0.0.0.0')
    _port = getenv('HBNB_API_PORT', 5000)
    app.run(host=_host, port=_port)
