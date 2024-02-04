#!/usr/bin/python3
"""The main app to run from."""

from api.v1.views import app_views
from flask import Flask
from os import getenv
from flask import jsonify
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Response for page not found"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close(exception=None):
    """close session at the end"""
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=int(port), threaded=True, debug=True)
