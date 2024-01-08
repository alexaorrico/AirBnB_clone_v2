#!/usr/bin/python3

from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """shows the status of a request"""
    status = {"status": "OK"}
    return jsonify(status)

@app_views.route('/api/v1/stats',strict_slashes=False)
def stats():
    """no. of each objects"""
    resources = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }
    stats = OrderedDict()
    for key in sorted(resources.keys()):
        count = storage.count(resources[key])
        if count > 0:
            stats[key] = count
    return jsonify(stats)
