#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request
import json


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    amenities_dict = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities_dict.values()]
    return amenities_list


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return amenity.to_dict(), 201
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenities_delete(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify('{}'), 201


@app_views.route('/amenities', methods=['POST'])
def amenities_post():
    try:
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        if 'name' not in data_object:
            abort(400, 'Missing name')
        new_amenity = Amenity(**data_object)
        storage.new(new_amenity)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenities_put(amenity_id):
    try:
        amenity_up = storage.get(Amenity, amenity_id)
        if not amenity_up:
            abort(404)
        data = request.get_data()
        data_object = json.loads(data.decode('utf-8'))
        for key, value in data_object.items():
            setattr(amenity_up, key, value)
        storage.save()
    except json.JSONDecodeError:
        abort(400, 'Not a JSON')
    return jsonify(amenity_up.to_dict()), 201
