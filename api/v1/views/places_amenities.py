#!/usr/bin/python3
"""Module for handling places amenities in the API"""

# Import statements
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Get amenity information for a specified place"""
    place_instance = storage.get("Place", place_id)
    if place_instance is None:
        abort(404)
    amenities_list = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objects = place_instance.amenities
    else:
        amenity_objects = place_instance.amenity_ids
    for amenity_instance in amenity_objects:
        amenities_list.append(amenity_instance.to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an amenity object from a place"""
    place_instance = storage.get("Place", place_id)
    amenity_instance = storage.get("Amenity", amenity_id)
    if place_instance is None or amenity_instance is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place_instance.amenities
    else:
        place_amenities = place_instance.amenity_ids
    if amenity_instance not in place_amenities:
        abort(404)
    place_amenities.remove(amenity_instance)
    place_instance.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """Adds an amenity object to a place"""
    place_instance = storage.get("Place", place_id)
    amenity_instance = storage.get("Amenity", amenity_id)
    if place_instance is None or amenity_instance is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place_instance.amenities
    else:
        place_amenities = place_instance.amenity_ids
    if amenity_instance in place_amenities:
        return jsonify(amenity_instance.to_dict())
    place_amenities.append(amenity_instance)
    place_instance.save()
    return make_response(jsonify(amenity_instance.to_dict()), 201)
