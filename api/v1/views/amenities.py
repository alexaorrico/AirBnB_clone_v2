#!/usr/bin/python3
"""Amenity objects that handle all default RESTFul API actions"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all amenity objects"""
    all_amenities = storage.all(Amenity).values()
    ls_amenities = []
    for amenity in all_amenities:
        ls_amenities.append(amenity.to_dict())
    return jsonify(ls_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a specific amenity Object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create a new amenity object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a specific amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")

        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        abort(404)
