#!/usr/bin/python3
'''index view for API'''
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns JSON """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    '''Number of each object by type'''
    return jsonify(
            amenities=storage.count('Amenity'),
            cities=storage.count('City'),
            places=storage.count('Place'),
            reviews=storage.count('Reviews'),
            states=storage.count('State'),
            users=storage.count('User')
        )
