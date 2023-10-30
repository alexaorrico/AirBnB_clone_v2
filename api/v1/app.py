#!/usr/bin/python3
"""Application module"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")


@app.teardown_appcontext
def tear_down(self):
    """closes query after each session"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """Returns a JSON-formatted 404 status code response"""
    response = {'error': "Not found"}
    return make_response(jsonify(response), 404)


if __name__ == "__main__":
    host = '0.0.0.0' if host is None else host
    port = '5000' if port is None else port

    app.run(host, port, threaded=True)
