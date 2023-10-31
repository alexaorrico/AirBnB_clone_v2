#!/usr/bin/python3
"""This script creates a new view for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Get all the amenity objects"""
    objs = storage.all(Amenity).values()
    return jsonify([amenities.to_dict() for amenities in objs])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get the amenity by id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """To deletes a amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """To creates a new amenity object"""
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    if 'name' not in request.get_json():
        abort(400, {'message': 'Missing name'})
    amenity = Amenity(**request.get_json())
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity object by id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, {'message': 'Not a JSON'})
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
