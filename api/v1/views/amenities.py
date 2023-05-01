#!/usr/bin/python3

'''
This module creates a new view for Amenity objects
Routes:
    GET /api/v1/amenities - Retrieves a list of all Amenity objects
    GET /api/v1/amenities/<amenity_id> - Retrieves a Amenity object
    DELETE /api/v1/amenities/<amenity_id> - Deletes a Amenity object
    POST /api/v1/amenities - Creates a Amenity
    PUT /api/v1/amenities/<amenity_id> - Updates a Amenity object
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''
    Retrieves the list of all Amenity objects
    '''
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    '''
    Retrieves an Amenity Object
    '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''
    Deletes an Amenity Object
    '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''
    Creates an Amnenity Object
    '''
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    amenity = Amenity(**body)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''
    Updates an Amenity Object
    '''
    amenity = storage.get(Amenity, amenity_id)
    body = request.get_json()
    if amenity is None:
        abort(404)
    if body is None:
        abort(400, 'Not a JSON')
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
