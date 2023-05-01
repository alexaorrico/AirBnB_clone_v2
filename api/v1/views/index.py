#!/usr/bin/python3
# Import necessary libraries
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# Create route to /status
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Return the jSON format of the status"""
    return jsonify({'status': 'OK'})


# Create route to /stats
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Get count of objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "citites", "places", "reviews", "states", "users"]

    obj_count = {}
    for i in range(len(classes)):
        obj_count[names[i]] = storage.count(classes[i])

    return jsonify(objs_count)
