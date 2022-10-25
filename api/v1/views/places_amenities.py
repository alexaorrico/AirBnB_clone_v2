#!/usr/bin/python3
"""Handle amenities route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, storage_t
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity information for all amenities in a specified place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    if storage_t == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids

    for amenity in place_amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity based on its id from a place based on its id"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids

    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return (jsonify({}))


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def add_place_amenity(place_id, amenity_id):
    """create a new place amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
