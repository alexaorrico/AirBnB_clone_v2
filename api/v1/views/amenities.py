#!/usr/bin/python3
'''BLueprint implementation for amenity model'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_amenities(amenity_id=None):
    '''Return the list of all Amenity objects'''
    if request.method == 'DELETE':
        return del_amenity(amenity_id)
    elif request.method == 'POST':
        return add_amenity()
    elif request.method == 'PUT':
        return update_amenity(amenity_id)
    elif request.method == 'GET':
        return get_amenities(amenity_id)


def get_amenities(amenity_id=None):
    '''Handles all get request to amenities endpoint'''
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())
    amenities_k = [val.to_dict() for val in storage.all(Amenity).values()]
    return jsonify(amenities_k)


def del_amenity(amenity_id):
    '''Deletes a amenity obj with amenity_id'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


def add_amenity():
    '''Adds amenity to amenities'''
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    amenity = Amenity(**req_data)
    amenity.save()
    return get_amenities(amenity.id), 201


def update_amenity(amenity_id):
    '''Update a amenity instance'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    for key, val in req_data.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(amenity, key, val)
    amenity.save()
    return get_amenities(amenity.id), 200
