#!/usr/bin/python3
""" Index """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """Retrieves the number"""
    stat = {}
    objs = {
            "Amenity": "amenities",
            "User": "users",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states"
        }
    for cls_name, key in objs.items():
        stat[key] = storage.count(eval(cls_name))

    return jsonify(stat)
