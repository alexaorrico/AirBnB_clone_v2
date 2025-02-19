#!/usr/bin/python3
"""
Defines route for status used to check api availability
"""

from api.v1.views.__init__ import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'])
def status():
    """Returns status of api"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def obj_count():
    """Returns counts of all objects"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage
    cls_to_lowerstr = {
        Amenity: "amenities",
        City: "cities",
        Place: "places",
        Review: "reviews",
        State: "states",
        User: "users"
    }
    count_dict = {}
    for k, v in cls_to_lowerstr.items():
        count_dict[v] = storage.count(k)
        print(count_dict)
    return jsonify(count_dict)
