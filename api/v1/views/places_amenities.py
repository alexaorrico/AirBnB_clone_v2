#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for amenities"""
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/amenities',
        methods=['GET'], strict_slashes=False)
def get_link_amenities(place_id):
    """
    Retrieves the list of all Amenity objects for a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_link_amenity(place_id, amenity_id):
    """
    Deletes an amenity object by place id and amenity id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    Link an amenity to a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 201)
