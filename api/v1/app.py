#!/usr/bin/python3
""" This is the app folder"""

from flask import Flask, Blueprint, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_close(self):
    """ Method to close """
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """Method no found page"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """ Run Flask Server """
    app.run(host=os.getenv('HBNB_API_HOST', "0.0.0.0"), port=os.getenv(
        'HBNB_API_PORT', 5000), threaded=True,  debug=True)
