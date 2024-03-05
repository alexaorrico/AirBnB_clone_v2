#!/usr/bin/python3
""" Amenity module """

from api.v1.views import app_views
from models.amenity import Amenity
from flask import abort, jsonify
from models import storage


@app_views.route('/amenities')
def all_amenities():
    """ Retrieves a list of all amenity objects """
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>')
