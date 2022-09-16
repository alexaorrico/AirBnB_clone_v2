#!/usr/bin/python3
"""Module with the view for Place - Amenity objects"""
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage
from flask import request, abort, jsonify


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def places_amenities(place_id):
    """Return a list of dictionaries of all amenities for a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def modify_amenities(place_id, amenity_id):
    """Delete or add an amenity instance to the place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        for amenities in place.amenities:
            if amenities.id == amenity.id:
                place.amenities.remove(amenity)
                storage.save()
                return {}, 200
        return jsonify(amenity.to_dict()), 200
    if request.method == 'POST':
        for amenities in place.amenities:
            if amenities.id == amenity.id:
                return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
