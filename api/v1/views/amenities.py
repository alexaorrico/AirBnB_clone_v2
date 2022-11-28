#!/usr/bin/python3
"""module amenities
Handles amenties objects for RestfulAPI
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves list of amenity objects"""
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenities in all_amenities:
        list_amenities.append(amenities.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity():
    """retrieves specific amenity"""
    amenity = storage.get(amenity, amenity_id)
    if not amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity():
    """deletes amenity object"""
    amenity = amenity.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)
