#!/usr/bin/python3
"""new view for Amenity objects that handles all default RESTFul API actions"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    all_amenities = []
    for amenity in storage.all(Amenity).values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_obj(amenity_id):
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    return jsonify(storage.get(Amenity, amenity_id).to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    storage.delete(storage.get(Amenity, amenity_id))
    storage.save()
    return {}, 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):

    existing_amenity = storage.get(Amenity, amenity_id)
    if existing_amenity is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in {'id', 'created_at', 'updated_at'}:
            setattr(existing_amenity, k, v)
    storage.save()
    return jsonify(existing_amenity.to_dict()), 200
