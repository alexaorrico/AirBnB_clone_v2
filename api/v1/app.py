#!/usr/bin/python3
"""Starts a flask session and imports blueprint"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)


app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown(self):
    """ handles teardown """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    return (jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    HBNB_API_PORT = getenv("HBNB_API_PORT", 5000)
    app.run(debug=True, host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
