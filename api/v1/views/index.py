#!/usr/bin/python3
""" Return status conexion app"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"amenities": "Amenity",  "cities": "City",
           "places": "Place", "reviews": "Review",
           "states": "State", "users": "User"}


@app_views.route('/status')
def status():
    """ return status"""
    return ({"status": "OK"})


@app_views.route('/stats')
def fun_count():
    """ return count obj """
    object = {}
    for key, value in classes.items():
        object[key] = storage.count(value)
    return jsonify(object)
