#!/usr/bin/python3
"""Amenity"""

from api.v1.views import app_views
from flask import jsoninfy, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', methods=['GET'])
def list_amenities():
    """List of amenities"""
    list_amenities = [obj].to_dict() fo obj in storage.all("Amenity").values()]
    return jsonify(list_amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Get Amenity"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
            if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete Amenity"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
            if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    amenity_obj.remove(amenity_obj[0])
    for obj in all_amenities:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """Create Amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updat_amenity(amenity_id):
    """Update Amenity"""
    all_amenities = storage.All("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
            if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    if not request.get_json():
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_obj[0]), 200
