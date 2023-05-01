#!/usr/bin/python3
"""
This module defines Flask routes for managing amenities for a given place.
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from os import environ

STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_per_place(place_id):
    """
    Retrieve all amenities of a given place
    """
    place = storage.get('Place', place_id)

    if place is None:
        abort(404)

    amenities = []
    all_amenities = storage.all('Amenity')

    if STORAGE_TYPE == 'db':
        amenities = place.amenities
    else:
        amenities_ids = place.amenity_ids
        amenities = [storage.get('Amenity', amenity_id) for amenity_id in amenities_ids]

    return jsonify([amenity.to_json() for amenity in amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST', 'DELETE'])
def link_amenity_to_place(place_id, amenity_id):
    """
    Link or unlink an amenity from a place
    """
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)

    if not place or not amenity:
        abort(404)

    if request.method == 'DELETE':
        if STORAGE_TYPE == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.pop(amenity_id, None)

        place.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if STORAGE_TYPE == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_json()), 200
            place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_json()), 200
            place.amenity_ids[amenity_id] = amenity.id

        place.save()
        return jsonify(amenity.to_json()), 201
