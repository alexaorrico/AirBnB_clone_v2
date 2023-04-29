#!/usr/bin/python3
"""This module contains the view for Amenity objects"""
from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from datetime import datetime


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """retrieves the list of all Amenity objects"""
    objects = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in objects.values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """retrieves a Amenity object using it's id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """deletes a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """creates a Amenity object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    obj = Amenity(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    data = request.get_json(silent=True)
    if not obj:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if (key in obj.__dict__ and key not in
                ['id', 'created_at', 'updated_at']):
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
