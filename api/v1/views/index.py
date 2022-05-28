#!/usr/bin/python3
""" Index view """
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Return the status of your API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Retrieves the number of each objects by type """
    obj = {'amenities': storage.count('Amenity'),
           'cities': storage.count('City'),
           'places': storage.count('Place'),
           'reviews': storage.count('Review'),
           'states': storage.count('State'),
           'users': storage.count('User')}
    return jsonify(obj)
