#!/usr/bin/python3
""" Index Module """


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}
plurals = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route("/status")
def get_status():
    """ Returns a status in JSON format """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def num_of_objs():
    """ Retrieves the number of each object by type """
    totals = {}
    for key, value in classes.items():
        for k, v in plurals.items():
            if value == v:
                totals[k] = storage.count(key)
    return jsonify(totals)
