#!/usr/bin/python3
""" Amenities """

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieve all Amenities of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route(
  '/places/<place_id>/amenities/<amenity_id>',
  methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route(
  '/places/<place_id>/amenities/<amenity_id>',
  methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Link a Amenity to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
