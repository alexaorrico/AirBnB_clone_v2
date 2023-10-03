#!/usr/bin/python3
"""
The index module
"""

from flask import jsonify, Blueprint
from models import storage
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Returns status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=["GET"])
def get_object_count():
    """Returns object count"""
    response = {
      "amenities": storage.count("Amenity"),
      "cities": storage.count("City"),
      "places": storage.count("Place"),
      "reviews": storage.count("Review"),
      "states": storage.count("State"),
      "users": storage.count("User")
    }

    return jsonify(response)
