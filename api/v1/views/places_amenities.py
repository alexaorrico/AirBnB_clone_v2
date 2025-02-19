#!/usr/bin/python3
""" places_amenities module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def all_amenities_place(place_id):
    """ get all amenities """
    place = storage.get('Place', place_id)
    all_amenities = []
    if not place:
        abort(404)
    for amenity in place.amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_place(place_id, amenity_id):
    """ delete an amenity """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return {}


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_a_place(place_id, amenity_id):
    """ link an amenity to a place """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return amenity.to_dict()
    place.amenities.append(amenity)
    storage.save()
    return amenity.to_dict(), 201
