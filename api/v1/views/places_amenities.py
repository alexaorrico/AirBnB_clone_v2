#!/usr/bin/python3
"""
Module for Place-Amenity view
"""

from api.v1.views import app_views
from models import storage, amenity, place
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def list_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    # Check if the place_id is linked to any Place object
    place_obj = storage.get(place.Place, place_id)
    if place_obj is None:
        abort(404)

    if storage_t == 'db':
        amenities = [amenity.to_dict() for amenity in place_obj.amenities]
    else:
        amenities = [amenity.to_dict() for amenity in place_obj.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def unlink_amenity_from_place(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    # Check if the place_id is linked to any Place object
    place_obj = storage.get(place.Place, place_id)
    if place_obj is None:
        abort(404)

    # Check if the amenity_id is linked to any Amenity object
    amenity_obj = storage.get(amenity.Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    if storage_t == 'db':
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)
    else:
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        place_obj.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    # Check if the place_id is linked to any Place object
    place_obj = storage.get(place.Place, place_id)
    if place_obj is None:
        abort(404)

    # Check if the amenity_id is linked to any Amenity object
    amenity_obj = storage.get(amenity.Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    if storage_t == 'db':
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict()), 200
        place_obj.amenities.append(amenity_obj)
    else:
        if amenity_id in place_obj.amenity_ids:
            return jsonify(amenity_obj.to_dict()), 200
        place_obj.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity_obj.to_dict()), 201
