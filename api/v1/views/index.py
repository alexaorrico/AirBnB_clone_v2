#!/usr/bin/python3
"""
create a route /status on the object app_views that returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """returns JSON of API status"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats", strict_slashes=False)
def storage_counts():
    """retrieves counts of each object by type"""
    obj_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
<<<<<<< HEAD
    for key, value in Obj_count.items():
        Obj_count[key] = storage.count(value)
    return jsonify(Obj_count)
=======

    obj_dict = {}
    for key, value in classes.items():
        obj_dict[key] = storage.count(value)

    return jsonify(obj_dict)
>>>>>>> f61419b9c8d53faeeaab2f7b00854c945df71058
