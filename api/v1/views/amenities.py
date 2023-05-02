#!/usr/bin/python3
"""
New view for Amenity objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/api/v1/amenities', strict_slashes=False)
def all_amenities():
    """ retrieve list of all Amenity objects """
    all_amenities = []
    for amenity in storage.all('Amenity').values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/api/v1/amenities/<amenity_id>', strict_slashes=False)
def retrieve_amenity(amenity_id):
    """ retrieve a particular Amenity """
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return amenity.to_dict()
    abort(404)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete an Amenity """
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return {}
    abort(404)


@app_views.route('/api/v1/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ create an Amenity """
    amenity_name = request.get_json()
    if not amenity_name:
        abort(400, {'Not a JSON'})
    if 'name' not in amenity_name:
        abort(400, {'Missing name'})
    new_amenity = Amenity(**amenity_name)
    storage.new(new_amenity)
    storage.save()
    return new_amenity.to_dict(), 201


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ update a Amenity """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_amenity = storage.get('Amenity', amenity_id)
    if not my_amenity:
        abort(404)
    for key, value in update_attr.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(my_amenity, key, value)
    storage.save()
    return my_amenity.to_dict()
