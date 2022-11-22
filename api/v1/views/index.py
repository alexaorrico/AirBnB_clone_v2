#!/usr/bin/python3
"""index file for app_views"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """GET /api/v1/status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """GET /api/v1/stats"""
    stats = jsonify({"amenities": storage.count(Amenity),
                     "cities": storage.count(City),
                     "places": storage.count(Place),
                     "reviews": storage.count(Review),
                     "states": storage.count(State),
                     "users": storage.count(User)})
    return stats
