#!/usr/bin/python3
'''
Import Blueprint to create routes for Amenity
'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    '''Get all Amenities'''
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def show_amenity(amenity_id):
    '''Show an amenity filter by id'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    '''Delete an amenity'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Create new amenity'''
    amenity = request.get_json()
    if not amenity:
        abort(400, {'Not a JSON'})
    if 'name' not in amenity:
        abort(400, {'Missing name'})
    new_amenity = Amenity(**amenity)
    storage.new(new_amenity)
    storage.save()
    return new_amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Update an amenity'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    req = request.get_json(silent=True)
    if req is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in req.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(amenity, k, v)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
