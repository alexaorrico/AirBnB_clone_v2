#!/usr/bin/python3
"""
This is the main flask api application file from which
our api runs
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(error=None):
    """method to close and cleanup the session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ method handler for resource not found(404)"""
    message = {
               "error": "Not found"
               }
    return make_response(jsonify(message), 404)


if __name__ == "__main__":
    api_host = os.environ.get('HBNB_API_HOST')
    api_port = int(os.environ.get('HBNB_API_PORT'))
    if not api_host:
        api_host = '0.0.0.0'
    if not api_port:
        api_port = 5000
    app.run(host=api_host, port=api_port, threaded=True)
