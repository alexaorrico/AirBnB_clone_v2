#!/usr/bin/python3
"""
Module: Status of your API, stats, and 404 err handler
return the status of API
"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# sets default port and host
port = getenv("HBNB_API_PORT", 5000)
host = getenv("HBNB_API_HOST", '0.0.0.0')

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)

# Cross-Origin Resource Sharing
cors = CORS(app, resources={r'/*': {'origins': host}})

@app.teardown_appcontext
def close_session(exception):
    """
    closes or otherwise deallocates the resource if it exists,
    Close the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found_err_handler(err):
    """
    error handler for 404 error
    Handles 404: not found error
    """
    # returns the err message and response status code
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(port=port,
            host=host,
            threaded=True)
