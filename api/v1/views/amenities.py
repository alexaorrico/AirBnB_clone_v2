#!/usr/bin/python3
""" Update amenities """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenities(amenity_id):
    """ Return a amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenities(amenity_id):
    """ Delete a amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def add_amenities():
    """ Add a amenity """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    amenity = Amenity(**request.json)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def update_amenities(amenity_id):
    """ Update a amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
