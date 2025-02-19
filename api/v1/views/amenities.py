#!/usr/bin/python3
'''amenities file'''
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenity():
    '''gets all amenities'''
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def req_amenity(amenity_id):
    '''gets a specific amenity'''
    try:
        amenity = storage.get(Amenity, amenity_id)
    except KeyError:
        abort(404)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    '''deletes a specific amenity'''
    try:
        amenity = storage.get(Amenity, amenity_id)
    except KeyError:
        abort(404)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    '''post a new amenity'''
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    '''updates an existing amenity'''
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    try:
        amenity = storage.get(Amenity, amenity_id)
    except KeyError:
        abort(404)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
