#!/usr/bin/python3
""" index module """


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class_dict = {
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User
        }

names_dict = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
        }


@app_views.route('/status', strict_slashes=False)
def status():
    """ return status of api """
    return jsonify({
            "status": "Ok"
        })


@app_views.route('stats', strict_slashes=False)
def count():
    """ returns count of all objects """
    dct = {}

    for item in class_dict:
        count = storage.count(class_dict[item])
        dct[names_dict[item]] = count

    return jsonify(dct)
