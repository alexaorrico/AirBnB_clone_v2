#!/usr/bin/python3
"""Implements RESTful actions for `Amenity` objects"""
from flask import jsonify, abort, make_response, request
from . import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def read_amenities(amenity_id=None):
    """Retrieves all `Amenity` objects or a single `Amenity` object"""

    if not amenity_id:
        return jsonify(
            [amenity.to_dict() for amenity in storage.all(Amenity).values()])

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a `Amenity` object"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates an `Amenity` object"""

    amenity_data = request.get_json(silent=True)
    if not amenity_data:
        abort(400, 'Not a JSON')

    if 'name' not in amenity_data:
        abort(400, 'Missing name')

    amenity = Amenity(name=amenity_data['name'])
    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an `Amenity` object"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity_data = request.get_json(silent=True)
    if not amenity_data:
        abort(400, 'Not a JSON')

    amenity.name = amenity_data.get('name', amenity.name)
    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 200)
