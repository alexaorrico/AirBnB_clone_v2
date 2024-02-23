#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON with status "OK"."""
    return jsonify(status="OK")


@app_views.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Retrieves the number of objects by type.
    """
    stats = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    }
    return jsonify(stats)
