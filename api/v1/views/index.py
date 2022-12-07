#!/usr/bin/python3
""" index """


from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/status', strict_slashes=False)
def jsmessage():
    return(jsonify({"status": "OK"}))


@app_views.route('/stats', strict_slashes=False)
def num_obj():
    return jsonify({
        "amenities": storage.count(classes["Amenity"]),
        "cities": storage.count(classes["City"]),
        "places": storage.count(classes["Place"]),
        "reviews": storage.count(classes["Review"]),
        "states": storage.count(classes["State"]),
        "users": storage.count(classes["User"])
        })