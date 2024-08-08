#!/usr/bin/python3
"""
Module defines a Flask application
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_error(error):
    """ Handles error 404 """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exception=None):
    """ Closes the storage """
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
