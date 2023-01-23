#!/usr/bin/python3
"""Main Entry Point for the API"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
CORS(app, origins='0.0.0.0')
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return make_response(jsonify(error="Not found"), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
