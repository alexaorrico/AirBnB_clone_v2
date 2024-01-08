#!/usr/bin/python3
"""flask app"""

from flask import Flask, make_response, jsonify
import models
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """remove the current session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handler for 404 errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """execute when run directly"""
    # get values of environment variables, default=0.0.0.0
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    # get values of environment variables, default=500
    port = getenv('HBNB_API_PORT', '5000')
    # run flask with specified host and post
    app.run(host=host, port=port, threaded=True)
