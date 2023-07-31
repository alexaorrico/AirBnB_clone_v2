#!/usr/bin/python3
"""
    Blueprint to all ALX Headache
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """returns status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_objects():
    """retrieves all objects by classes"""
    return jsonify({"amenities": storage.count(Amenity),\
    "states": storage.count(State), "places": storage.count(Place
    ), "cities": storage.count(City), "reviews": storage.count(
    Review), "users": storage.count(User)})
 #   Dictionary = {"City": City, "Place": Place, "Review": Review, "State": State, "User": User}
 #   new_dict = {}
#    for key, val in Dictionary.items():
#        if storage.classes.get(key):
#            count = storage.count(val)
#            new_dict[key.lower()] = count
#
#    for key, val in new_dict.items():
#        if key.endswith('y'):
#            new_dict[key[:-1] + 'ies'] = new_dict.pop(key)
#        else:
#            new_dict[key + 's'] = new_dict.pop(key)
#    return jsonify(new_dict)
