#!/usr/bin/python3
"""index """

from models import storage
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """retrun status json"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """retrun the number of each objects by type"""

    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    res = {}
    for key, cls in classes.items():
        res[key] = storage.count(cls)
    return jsonify(res)
