#!/usr/bin/python3
""" Module that returns an object """


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes


@app_views.route('/status')
def status():
    """
    Return status ok
    Returns:
        json: status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def number_obje():
    """Retrieves the number of each objects by type"""
    obje = {"amenities": storage.count(classes["Amenity"]),
            "cities": storage.count(classes["City"]),
            "places": storage.count(classes["Place"]),
            "reviews": storage.count(classes["Review"]),
            "states": storage.count(classes["State"]),
            "users": storage.count(classes["User"])}
    return jsonify(obje)
