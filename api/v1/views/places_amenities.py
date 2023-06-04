#!/usr/bin/python3
"""This module defines a view for the link between Place and Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_t == 'db':
        amenities = place.amenities
    else:
        amenities = [storage.get(Amenity, amenity_id)
                     for amenity_id in place.amenity_ids]
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def place_amenity(place_id, amenity_id):
    """Deletes or links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if request.method == 'DELETE':
        if storage_t == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST':
        if storage_t == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
