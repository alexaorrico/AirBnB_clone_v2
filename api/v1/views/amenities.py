#!/usr/bin/python3
"""Amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def list_amenities():
    '''Retrieves a list of all Amenity objects'''
    amentities_list = [obj.to_dict()
                       for obj in storage.all("Amenity").values()]
    return jsonify(amentities_list)


@app_views.route(
    '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False
)
def get_amenity(amenity_id):
    '''Retrieves an Amenity object'''
    all_amenities = storage.all("Amenity").values()
    amen_obj = [obj.to_dict() for obj in all_amenities
                if obj.id == amenity_id]
    if amen_obj == []:
        abort(404)
    return jsonify(amen_obj[0])


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False
)
def delete_amenity(amenity_id):
    '''Deletes an Amenity object'''
    all_amens = storage.all("Amenity").values()
    amen_obj = [obj.to_dict() for obj in all_amens
                if obj.id == amenity_id]
    if amen_obj == []:
        abort(404)
    amen_obj.remove(amen_obj[0])
    for obj in all_amens:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route(
    '/amenities/', methods=['POST'], strict_slashes=False
)
def create_amenity():
    '''Creates an Amenity'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amens = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amens.append(new_amenity.to_dict())
    return jsonify(amens[0]), 201


@app_views.route(
    '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False
)
def updates_amenity(amenity_id):
    '''Updates an Amenity object'''
    all_amens = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in all_amens
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_obj[0]['name'] = request.json['name']
    for obj in all_amens:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_obj[0]), 200
