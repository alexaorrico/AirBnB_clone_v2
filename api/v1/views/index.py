#!/usr/bin/python3
"""

Flask web server creation to handle api petition-requests

"""
from flask import Response, jsonify
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes


@app_views.route('/status')
def check_status():
    """
    Commit changes in database
    """
    status_dict = {"status": "OK"}
    return jsonify(status_dict)


@app_views.route('/stats')
def num_objs():
    """
    Retrieves the number of each objects by type
    """
    objs = {"amenities": storage.count(classes["Amenity"]),
            "cities": storage.count(classes["City"]),
            "places": storage.count(classes["Place"]),
            "reviews": storage.count(classes["Review"]),
            "states": storage.count(classes["State"]),
            "users": storage.count(classes["User"])}
    return jsonify(objs)
