#!/usr/bin/python3
""" This script comprises a flask application """


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route("/status")
def _json():
    _dict = {"status": "OK"}
    return jsonify(_dict)


@app_views.route("/stats")
def _count():
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }

    _dic = {key: storage.count(val) for key, val in classes.items()}
    return jsonify(_dic)
