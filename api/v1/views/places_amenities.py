#!/usr/bin/python3
"""
Handles all default RESTful API actions for Place objects
"""

from . import app_views
from models import storage, storage_t
from models.user import User
from models.place import Place
from models.review import Review
from flask import abort, jsonify, make_response, request


@app_views.route("/places/<place_id>/amenities", methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves the list of all Reviews objects attached to a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route(
   "/places/<place_id>/amenities/<amenity_id>", methods=['DELETE']
)
def del_place_amenity(place_id, amenity_id):
    """Deletes a review given its ID"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)
    place.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """Creates a review"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    if storage_t == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
