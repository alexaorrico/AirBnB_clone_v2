#!/usr/bin/python3
"""index """

from models import storage, storage_t
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity


@app_views.route("places/<place_id>/amenities", methods=['GET', 'POST'])
def place_amenities_without_id(place_id=None):
    """Create a new place or return all the cities"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        amenity_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenity_list), 200


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=['POST', 'DELETE'])
def place_amenities_with_id(place_id=None, amenity_id=None):
    """Perform READ UPDATE DELETE operations on a place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None or place is None:
        abort(404)
    place_amenities_ids = [amenity.id for amenity in place.amenities]

    if request.method == 'DELETE':
        if amenity_id not in place_amenities_ids:
            abort(404)
        if storage_t == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.pop(amenity.id)
        place.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity_id in place_amenities_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
