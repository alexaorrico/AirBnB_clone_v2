#!/usr/bin/python3


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns the status as JSON."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieve the number of each object type."""
    stats = {}
    classes = ["User", "State", "City", "Amenity", "Place", "Review"]

    for cls in classes:
        count = storage.count(cls)
        stats[cls] = count

    return jsonify(stats)
