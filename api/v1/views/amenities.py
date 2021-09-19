#!/usr/bin/python3
"""Amenities in api v1"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_all_amenities():
    """
        All amenity objects
    """
    return jsonify([amenity.to_dict() for amenity in \
            storage.all(Amenity).values()]), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity_by_id(amenity_id):
    """
        An amenity object based on its id. Error if not found
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """
        Updates information of amenity
    """
    keys = ['id', 'created_at', 'updated_at']
    amenity_json = request.get_json(silent=True)

    if not amenity_json:
        return jsonify({'error': 'Not a JSON'}), 400
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    for key, val in amenity_json.items():
        if key not in keys:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """
        Stores and returns a new amenity
    """
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in amenity_json:
        return jsonify({'error': 'Missing name'}), 400
    amenity = Amenity(**amenity_json)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """
        Deletes an amenity with a id and returns an empty JSON
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200
