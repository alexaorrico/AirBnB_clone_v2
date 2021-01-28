#!/usr/bin/python3
"""Modules that handles all Restful API actions For Amenities"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retreives the list of all the amenities"""
    amenities = []
    all_amenities = storage.all(Amenity).values()
    for amenity in all_amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """Returns an object amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a given amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates a new given amenity"""
    new_amenity = request.get_json()
    if not new_amenity:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in new_amenity:
        return jsonify({'error': 'Missing name'}), 400
    else:
        new_obj = Amenity(**new_amenity)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update a given amenity"""
    amenity_to_update = request.get_json()
    if not amenity_to_update:
        return jsonify({'error': 'Not a JSON'}), 400

    my_dict = storage.get(Amenity, amenity_id)
    if my_dict:
        for key, value in amenity_to_update.items():
            setattr(my_dict, key, value)
        storage.save()
        return jsonify(my_dict.to_dict()), 200
    else:
        abort(404)
