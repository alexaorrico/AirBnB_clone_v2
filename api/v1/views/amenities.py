#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """return all the amenities in the database"""
    amenities_list = []

    for amenity in storage.all(Amenity).values():
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """return a amenity by id in the database"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a amenity by id in the database"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """create a new amenity in the database"""
    try:
        amenity_dict = request.get_json()
        if 'name' not in amenity_dict:
            return 'Missing name', 400

        new_amenity = Amenity(**amenity_dict)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201
    except Exception:
        return 'Not a JSON', 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update a amenity by id in the database"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    try:
        amenity_dict = request.get_json()
    except Exception:
        return 'Not a JSON', 400

    if not amenity_dict:
        return 'Not a JSON', 400

    ignored_keys = ['id', 'created_at', 'updated_at']

    for key, value in amenity_dict.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)

    amenity.save()

    return jsonify(amenity.to_dict()), 200
