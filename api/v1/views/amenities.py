#!/usr/bin/python3
'''Create a new view for Amenity objects that handles all default
RESTFul API actions'''
from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    '''Retrieves the list of all Amenity objects'''
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenities_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    '''Retrieves a Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/menities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes a Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Creates a Amenity object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates a Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, val in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, val)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
