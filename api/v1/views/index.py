#!/usr/bin/python3
""" show status """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ object app_views that returns a JSON """
    app_views = {'status': 'OK'}
    return jsonify(app_views)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ endpoint that retrieves the number of each objects """
    class_stat = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(class_stat)
