#!/usr/bin/python3
""" index """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns a JSON """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    clases = {"amenities": Amenity, "cities": City, "places": Place,
              "reviews": Review, "states": State, "users": User}
    my_dict = {}
    for i, j in clases.items():
        my_dict[i] = storage.count(j)
    return jsonify(my_dict)
