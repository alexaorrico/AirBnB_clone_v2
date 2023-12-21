#!/usr/bin/python3
"""index module with flask app rutes for status
and stats"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status')
def status():
    """returns the API status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """use count method to count obj"""
    dict = {}

    for cls, class_list in classes.items():
        counter = storage.count(cls)
        dict[cls] = counter

    return jsonify(dict)
