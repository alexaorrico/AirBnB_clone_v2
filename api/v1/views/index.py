#!/usr/bin/python3
"""index page"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """return: status ok"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def cls_obj_count():
    """retrieves the number of each objects by type"""
    class_dict = {"amenities": Amenity, "cities": City, "places": Place,
                  "reviews": Review, "states": State, "users": User}
    data = dict()
    for k, v in class_dict.items():
        n = storage.count(v)
        # add to data dict
        data[k] = n

    return jsonify(data)
