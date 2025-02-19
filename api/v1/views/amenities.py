#!/usr/bin/python3
"""Amenity management endpoints"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    '''Fetches all Amenity objects'''
    amenities_list = [item.to_dict() for item in \
       storage.all("Amenity").values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    '''Fetches a specific Amenity object by ID'''
    all_amenities = storage.all("Amenity").values()
    matching_amenity = [item.to_dict() for item in all_amenities if \
       item.id == amenity_id]
    if not matching_amenity:
        abort(404)
    return jsonify(matching_amenity[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes a specific Amenity object by ID'''
    all_amenities = storage.all("Amenity").values()
    matching_amenity = [item.to_dict() for item in all_amenities if \
       item.id == amenity_id]
    if not matching_amenity:
        abort(404)
    matching_amenity.remove(matching_amenity[0])
    for item in all_amenities:
        if item.id == amenity_id:
            storage.delete(item)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    '''Creates a new Amenity object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities_list = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities_list.append(new_amenity.to_dict())
    return jsonify(amenities_list[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    '''Updates an existing Amenity object'''
    all_amenities = storage.all("Amenity").values()
    matching_amenity = [item.to_dict() for item in all_amenities if \
       item.id == amenity_id]
    if not matching_amenity:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    matching_amenity[0]['name'] = request.json['name']
    for item in all_amenities:
        if item.id == amenity_id:
            item.name = request.json['name']
    storage.save()
    return jsonify(matching_amenity[0]), 200
