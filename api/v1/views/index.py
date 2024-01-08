#!/usr/bin/python3
"""
Module docs
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def page_status():
    """
    function to handle status of webpage
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def obj_stats():
    """
    function to handle state/route
    """
    objs = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
            }
    return jsonify(objs)


if __name__ == "__main__":
    pass
