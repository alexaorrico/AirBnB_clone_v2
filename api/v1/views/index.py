#!/usr/bin/python3
"""
Module: index
"""
from api.v1.views import app_views, storage
from flask import jsonify
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status/', strict_slashes=False)
def status():
    """ returns status: OK JSON  """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats():
    """ returns number of objects by type  """
    class_counts = {}
    convert_dict = {
        'Amenity': 'amenities',
        'State': 'states',
        'City': 'cities',
        'User': 'users',
        'Place': 'places',
        'Review': 'reviews'
    }

    for _class in convert_dict.keys():
        class_counts[convert_dict[_class]] = storage.count(_class)

    return jsonify(class_counts)
