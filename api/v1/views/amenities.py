#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amentity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    
    if not request.is_json:
        abort(400, 'Not a JSON')
    
    data = request.get_json()

    ignored_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200