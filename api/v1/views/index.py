#!/usr/bin/python3

"""
create a route /status on the object app_views
returns a JSON "status": "OK"
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """
    returns JSON: "status": "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """
    retrieves the number of each objects by type
    """
    obj_count = {
            "amenities": storage.count('Amenities'),
            "cities": storage.count('Cities'),
            "places": storage.count('Places'),
            "reviews": storage.count('Reviews'),
            "states": storage.count('States'),
            "users": storage.count('Users')
            }
    return jsonify(obj_count)
