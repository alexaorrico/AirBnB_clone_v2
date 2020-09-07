#!/usr/bin/python3
""" index """
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
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
