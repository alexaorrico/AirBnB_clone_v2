#!/usr/bin/python3
"""API and Index Module"""

from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'OK'})

@app_views.route('/stats', strict_slashes=False)
def count():
    """
    returns a count of all database objects
    """

    models_avail = {
        "User": "users",
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
    }
    mod_objs = [Amenity, City, Place, Review, State, User]

    count = {models_avail[cls]: storage.count(obj) for cls, obj in enumerate(mod_objs)}

    return jsonify(count)
