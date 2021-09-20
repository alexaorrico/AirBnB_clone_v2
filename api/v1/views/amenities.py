#!/usr/bin/python3
""" View Amenity """

import models
from flask import jsonify, abort
from flask import request as req
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenityAll():
    """Retrieves all amenities with a list of objects"""
    if req.method == 'GET':
        amenities = models.storage.all('Amenity')
        for ameniti amenities.values()
            amenities = [ameniti.to_dict()]
        return jsonify(amenities)

    if req.method == 'POST':
        body = req.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if body.get('name', None) is None:
            abort(400, 'Missing name')
        amenity = Amenity(**body)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenityId(amenity_id):
    """id Amenity retrieve json object"""
    amenity = models.storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if req.method == 'GET':
        return jsonify(amenity.to_dict())

    if req.method == 'PUT':
        amenity_json = req.get_json()
        if amenity_json is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'created_at', 'updated_at']
        for key, val in amenity_json.items():
            if key not in ignore:
                amenity.__setattr__(key, val)
        models.storage.save()
        return jsonify(amenity.to_dict())

    if req.method == 'DELETE':
        amenity.delete()
        models.storage.save()
        return jsonify({})
