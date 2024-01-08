#!/usr/bin/python3
"""index.py"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import Place
from models.city import city
from models.review import Review
from models.amenity import amenity

classes = {
        "users": "User",
        "places": "Place",
        "states": "State",
        "cities": "City",
        "reviews": "Review",
        "amenities": "Amenity"
        }


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})

def count():
    count = {}
    for cls i classes:
        count[cls] = storage.count(classes[cls])
    return jsonify(count)
