#!/usr/bin/python3
"""new view for Amenity objects that handles
all default RestFul API actions"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_allAmenity():
    """Retrieve a list of Amenities objects"""
    obj_dic = storage.all("Amenity")
    return jsonify([amenities.to_dict() for amenities in obj_dic.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a specific amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Delete a specific amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a amenity object"""
    if request.get_json() is None:
        return "Not a JSON", 400
    elif 'name' not in request.get_json():
        return "Missing name", 400
    else:
        amenity = Amenity(**request.get_json())
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def uptade_amenity(amenity_id):
    """Update a amenity store into storage"""
    if request.get_json() is None:
        return "Not a JSON", 400
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
