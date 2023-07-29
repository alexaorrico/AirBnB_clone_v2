#!/usr/bin/python3
"""
app.py
This module creates a variable app that is an instance of Flask and
registers the blueprint app_views to your Flask instance app
"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from api.v1.views import state_views
from api.v1.views import amenity_views

import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
app.register_blueprint(state_views, url_prefix="/api/v1/states",
                       name='state_views')
app.register_blueprint(amenity_views, url_prefix="/api/v1/amenities",
                       name='amenitiy_views')


@app.teardown_appcontext
def teardown_db(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def handle_not_found(err):
    """ returns a JSON-formatted 404 status code response """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    if "HBNB_API_HOST" in os.environ:
        host = os.getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"

    if "HBNB_API_PORT" in os.environ:
        port = os.getenv("HBNB_API_PORT")
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True)
