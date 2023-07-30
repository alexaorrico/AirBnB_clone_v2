#!/usr/bin/python3
"""amenity obj API"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_in_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """Get all amenities or a amenities whose id is specified"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Delete a amenity object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity(place_id):
    """Create a new amenity"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = request.get_json()
    if not amenity:
        abort(400, description="Not a JSON")
    if 'user_id' not in amenity:
        abort(400, description="Missing user_id")
    user = storage.get(User, amenity.get('user_id'))
    if user is None:
        abort(404)
    if 'text' not in amenity:
        abort(400, description="Missing text")
    amenity['place_id'] = place_id
    obj = amenity(**amenity)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Update a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    fixed_data = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if amenity is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in fixed_data:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
