#!/usr/bin/python3
"""API endpoint"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import os

@app_views.route('places/<place_id>/amenities', method=['GET'], strict_slashes=False)
def all_place_review(place_id):
    """Return list of all review objects of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
        for amenity in amenities:
            return jsonify(amenity.to_dict())
    else:
        amenity_ids = place.amenity_ids
        amenities = [storage.get(Amenity, amenity_id) for amenity_id in amenity_ids]
        return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """Deletes amenity object to a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amemity = place.amenities
    else:
        place_amenity = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)

    place_amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_place(place_id, amenity_id):
    """link amenity object to a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids

    if amenity in place_amenities:
        return jsonify(amenity.to_dict()), 200
    place_amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
