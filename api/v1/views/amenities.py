#!/usr/bin/python3
"""
Task 9
Create a new view for Amenity objects
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/api/v1/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    all_amenities = []
    for amenity in storage.all('Amenity').values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_amenity(amenity_id):
    """Retrieves an Amenity"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity """
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/api/v1/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates an Amenity """
    amenity_name = request.get_json()
    if not amenity_name:
        abort(400, {'Not a JSON'})
    if 'name' not in amenity_name:
        abort(400, {'Missing name'})
    new_amenity = Amenity(**amenity_name)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity """
    update_obj = request.get_json()
    if not update_obj:
        abort(400, {'Not a JSON'})
    this_amenity = storage.get('Amenity', amenity_id)
    if not this_amenity:
        abort(404)
    for key, value in update_obj.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(this_amenity, key, value)
    storage.save()
    return jsonify(this_amenity.to_dict())
