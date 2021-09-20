#!/usr/bin/python3
""" View Amenity """

import models
from flask import jsonify, abort
from flask import request
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenity_objects():
    """Returns amenity objects as JSON response"""
    if method == 'GET':
        amenities = models.storage.all('Amenity')
        amenities = [am.to_dict() for am in amenities.values()]
        return jsonify(amenities)

    if method == 'POST':
        body = get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if body.get('name', None) is None:
            abort(400, 'Missing name')
        amenity = Amenity(**body)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenity_res(amenity_id):
    """Returns a Amenity object as JSON response"""
    amenity = models.storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if method == 'GET':
        return jsonify(amenity.to_dict())

    if method == 'PUT':
        amenity_json = get_json()
        if amenity_json is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'created_at', 'updated_at']
        for key, val in amenity_json.items():
            if key not in ignore:
                amenity.__setattr__(key, val)
        models.storage.save()
        return jsonify(amenity.to_dict())

    if method == 'DELETE':
        amenity.delete()
        models.storage.save()
        return jsonify({})
