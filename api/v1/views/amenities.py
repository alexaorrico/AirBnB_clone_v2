#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request
from models import storage, amenity


@app_views('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenity = storage.all(amenity).values()
    amenity_list = []
    for amenity in amenity:
        amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)

@app_views('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a amenity object"""
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict()), 200

@app_views('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes amenity object"""
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates amenity object"""
    if not request.get_json():
        return jsonify({"error": "Not a Json"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    amenity = amenity(**request.get_json()), 201
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates amenity object"""
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if not request.get_json():
        return jsonify({"error": "Not a Json"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
