#!/usr/bin/python3
"""
Route definitions for the "Amenity" view
"""
from api.v1.views import app_views
from flask import request, jsonify, make_response, abort
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def list_place_amenities(place_id):
    """List amenities in a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete an amenity from a place's record"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity_ids = [a.id for a in place.amenities]
    if amenity_id not in amenity_ids:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """Create a new amenity in a place's record"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity_ids = [a.id for a in place.amenities]
    if amenity_id in amenity_ids:
        return make_response(jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 201)
