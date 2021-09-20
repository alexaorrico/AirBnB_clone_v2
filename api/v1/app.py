#!/usr/bin/python3
"""" API """
from os import getenv

from flask.json import jsonify
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import Blueprint

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
