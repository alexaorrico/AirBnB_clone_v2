#!/usr/bin/python3
"""
Create a new view for Amenity objects that
handles all default RESTFul API actions
"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()
        ]
    return jsonify(amenities), 200


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity()
    new_amenity.name = data['name']
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity_id(amenity_id):
    data = request.get_json()

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenities_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
