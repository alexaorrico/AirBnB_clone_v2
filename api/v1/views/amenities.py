#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""view for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def list_amenities():
    """Retrieves the list of all Amenity objects"""
    list_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by id"""""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object by id"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    amenity_obj.remove(amenity_obj[0])
    for obj in all_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity"""
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


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updates_amenity(amenity_id):
    """Updates a Amenity object by id"""
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_obj[0]['name'] = request.json['name']
    for obj in all_amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_obj[0]), 200
