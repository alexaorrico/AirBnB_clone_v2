#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/api/v1/amenities', methods=['GET'])
def all_amenties():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)

@app_views.route('/api/v1/amenities/<amenity_id>', methods=['GET'])
def by_id(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """del amenties"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/api/v1/amenities', methods=['POST'])
def create_amn():
    """by dict"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/api/v1/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    js = request.get_json()
    if not js:
        abort(400, 'Not a JSON')

    keys = ['id', 'created_at', 'updated_at']

    for key, value in js.items():
        if key not in keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
