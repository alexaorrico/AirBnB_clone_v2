#!/usr/bin/pythone3
""" module returns a JSON:OK"""
from models import storage
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views


clases = {"amenities": "Amenity", "cities": "City", "places": "Place",
          "reviews": "Review", "states": "State", "users": "User"}


@app_views.route('/status', strict_slashes=False)
def status():
    """returns a JSON: OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def num_obj():
    """num_objects"""
    obj_dict = {}
    for key, value in obj_text.items():
        obj_dict[key] = storage.count(value)
    return jsonify(obj_dict)


if __name__ == "__main__":
    pass
