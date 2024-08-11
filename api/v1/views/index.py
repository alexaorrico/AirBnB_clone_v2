#!/usr/bin/python3
""" A module containin routes in the index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def check_status():
    """ Returns the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    " Retrieves the number of each objects by type """
    from models.amenity import Amenity
    from models.city import City
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.review import Review

    classes = {"Amenity": Amenity, "City": City, "Place": Place,
               "Review": Review, "State": State, "User": User}
    all_cls = {}
    for key, classs_name in classes.items():
        value = storage.count(classs_name)
        all_cls[key] = value
    return jsonify(all_cls)
