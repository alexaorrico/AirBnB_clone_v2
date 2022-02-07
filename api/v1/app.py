#!/usr/bin/python3
"""This is the flask app"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_storage(self):
    """close the db session"""
    storage.close()


@app.errorhandler(404)
def error_handler(self):
    """return a json if error 404"""
    return make_response(jsonify({"error": "Not found"})), 404


if __name__ == "__main__":
    hbnb_api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    hbnb_api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=hbnb_api_host, port=int(hbnb_api_port),
            threaded=True, debug=True)
