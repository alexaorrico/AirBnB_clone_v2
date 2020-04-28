#!/usr/bin/python3
""" Starts a Flash Web Application """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from json import dumps


@app_views.route('/status')
def status():
    """returns a JSON: "status": "OK"""
    status_dict = {"status": "OK"}
    status_dict = dumps(status_dict, indent=4)
    return (status_dict)


@app_views.route('/stats')
def stats():
    """returns a JSON: "status": "OK"""
    classes = {"Amenity": Amenity, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}
    dict_count = {}
    count = 0
    for value in classes.values():
        count = storage.count(value)
        dict_count[value.__name__] = count
    dict_count = dumps(dict_count, indent=4)
    return (dict_count)
