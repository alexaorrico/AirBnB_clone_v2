#!/usr/bin/python3
""" Index file for api/v1
"""

from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ return status """
    return {"status": "OK"}


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieves the number of each objects by type
    """
    objects = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    return jsonify({key: storage.count(obj) for key, obj in objects.items()})
