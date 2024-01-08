#!/usr/bin/python3
"""
Create a route `/status` on the object app_views.
"""
# Import the required modules
from api.v1.views import app_views
from flask import jsonify
from models import storage

hbnbStats = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def api_status():
    """
    Returns a JSON response for RESTful API status.
    """
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """
    Retrieves the number of each objects by type.
    """
    return_dict = {}
    for key, value in hbnbStats.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)


if __name__ == "__main__":
    pass
