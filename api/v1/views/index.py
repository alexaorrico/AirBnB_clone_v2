#!/usr/bin/python3
''' comment  '''

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''  returns a JSON response '''
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def stats():
    ''' endpoint that retrieves the number of each objects by type '''
    classes = {
            "Amenities": storage.count('Amenity'),
            "Cities": storage.count('City'),
            "Places": storage.count('Place'),
            "Reviews": storage.count('Review'),
            "States": storage.count('State'),
            "Users": storage.count('User')
            }
    return jsonify(classes)
