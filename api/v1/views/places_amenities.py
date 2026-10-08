#!/usr/bin/python3
"""Amenities API"""
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """get method for amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if (getenv("HBNB_TYPE_STORAGE") == "db"):
        amenities = place.amenities
    else:
        amenities = place.amenities()
    place_amenity = []
    for amenity in amenities.values():
        place_amenity.append(amenity.to_dict())
    return jsonify(place_amenity)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_linked_amenity(place_id, amenity_id):
    """Delete an amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if (amenity.place_id != place_id):
        abort(404)
    amenity.delete()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Link Amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if (amenity.place_id == place_id):
        return jsonify(amenity.to_dict()), 200
    else:
        amenity.place_id = place_id
    return jsonify(amenity.to_dict()), 201
