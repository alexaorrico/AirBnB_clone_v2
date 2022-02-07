#!/usr/bin/python3
"""view for place and amenity link"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.review import Review


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def all_amenities_(place_id):
    """Retrieves the list of all amenities of a place given an ID"""
    amenities_list = []
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    for review in place.amenities:
        amenities_list.append(review.to_dict())
    return jsonify(amenities_list)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_amenity_in_place(place_id, amenity_id):
    """Deletes a amenity object in a place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['POST'],
    strict_slashes=False
    )
def create_amenity_places(place_id, amenity_id):
    """Create a amenity object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    if obj in place.amenities:
        return jsonify(obj.to_dict()), 200
    place.amenities.append(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201
