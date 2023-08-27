#!/usr/bin/python3
""" View for Amenities """

from flask import jsonify, request, abort
from models import Amenity
from api.v1.views import app_views


@app_views.route('/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Retrieve the list of all Amenity objects"""
    amenities = Amenity.query.all()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a specific Amenity object by its ID"""
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a specific Amenity object by its ID"""
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    return jsonify({})


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a specific Amenity object by its ID"""
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    keys_to_ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
