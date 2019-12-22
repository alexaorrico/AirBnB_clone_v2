#!/usr/bin/python3
"""
Views for Place - Amenity
"""
from flask import request, abort, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def amenities_place():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'GET':
        list_amenities = []
        place = storage.all('Place').values()
        if place:
            for amenity in place.amenities:
                list_amenities.append(amenity.to_dict())
            return jsonify(list_amenities), 200
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def amenity(place_id=None, amenity_id=None):
    """
    Retrieves the list of all Amenity objects: GET /api/v1/states
    Creates a State: POST /api/v1/states
    """
    if request.method == 'DELETE':
        place = storage.get('Place', place_id)
        amenity = storage.get('Amenity', amenity_id)
        if place and amenity and amenity_id in place.amenities:
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200
        abort(404)

    if request.method == 'POST':
        place = storage.get('Place', place_id)
        amenity = storage.get('Amenity', amenity_id)
        if place and amenity and amenity_id not in place.amenities:
            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
