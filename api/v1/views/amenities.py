#!/usr/bin/python3
"""
Amenity view objects that handle RESTFul API
"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
import models
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def status():
    """Gets list of amenities"""
    
    list = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        list.append(amenity.to_dict())
    return jsonify(list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get(amenity_id):
    """Gets an amenity obj"""

    amenities = storage.all(Amenity)
    id = f"Amenity.{amenity_id}"
    if id not in amenities:
        abort(404)

    amenity = amenities[id]
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete(amenity_id):
    """Deletes amenity obj"""

    amenities = storage.all(Amenity)
    id = f'Amenity.{amenity_id}'
    if id not in amenities:
        abort(404)

    amenity = amenities[id]
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post():
    """Creates an amenity obj"""

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    amenity = Amenity(name=data['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put(amenity_id):
    """Upgrades an amenity obj"""

    data = request.get_json()
    amenities = storage.all(Amenity)
    id = f"Amenity.{amenity_id}"
    if id not in amenities:
        abort(400)
    if not data:
        abort(400, 'Not a JSON')

    amenity = amenities[id]
    dict = amenity.__dict__

    for i in data:
        if amenity not in ['id', 'created_at', 'updated_at']:
            amenity[i] = data[i]

        storage.save()
        return jsonify(dict.to_dict()), 200