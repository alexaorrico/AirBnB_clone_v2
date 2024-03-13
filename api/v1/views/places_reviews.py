#!/usr/bin/python3
""" Place Reviews Module """

from api.v1.views import app_views
from flask import abort, Flask, jsonify, make_response
from models.amenity import Amenity
from models.place import place_amenity, Place


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get(place_id):
    """ Returns a list of Reviews objects """
    
