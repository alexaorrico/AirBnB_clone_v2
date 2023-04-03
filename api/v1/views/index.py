#!/usr/bin/python3
"""Create a route on the object app_views that returns a JSON: "status":OK """
from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Returns the count of each object type"""
    stats = {"amenities": storage.count("Amenity"),
             "cities": storage.count("City"),
             "places": storage.count("Place"),
             "reviews": storage.count("Review"),
             "states": storage.count("State"),
             "users": storage.count("User")}
    return jsonify(stats)
