#!/usr/bin/python3
"""
Module for the places_amenities view.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities_of_place(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities_list = []
    if storage.__class__.__name__ == 'DBStorage':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
        amenities = storage.all("Amenity").values()
        for amenity in amenities:
            if amenity.id in place.amenity_ids:
                amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """
    Deletes an Amenity object from a Place
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an Amenity object to a Place
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
