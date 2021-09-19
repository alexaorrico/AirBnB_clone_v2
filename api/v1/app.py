#!/usr/bin/python3
"""
    Start of API module

"""

from flask_cors import CORS
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(error):
    """ Calls the close method from storage """
    storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    """ Will return a 404 json query """
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    """ Only executes as main """
    api_host = getenv("HBNB_API_HOST")
    if not api_host:
        api_host = "0.0.0.0"
    api_port = getenv("HBNB_API_PORT")
    if not api_port:
        api_port = "5000"
    app.run(host=api_host, port=api_port, threaded=True)
