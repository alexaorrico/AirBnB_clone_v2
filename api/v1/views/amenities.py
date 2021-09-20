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
        amenities = [am.to_dict() for am in amenities.values()]
        return jsonify(amenities)

    if req.method == 'POST':
        body = req.get_json()
        if body is None:
            abort(400, 'Not a JSON')
        if body.get('name', None) is None:
            abort(400, 'Missing name')
        new_state = State(**body)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201



@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenityId(amenity_id):
    """id Amenity retrieve json object"""
    amenity = models.storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if req.method == 'GET':
        return jsonify(amenity.to_dict())

    if req.method == 'PUT':
        ame_json = req.get_json()
        if ame_json is None:
            abort(400, 'Not a JSON')
        ignore = ['id', 'created_at', 'updated_at']
        for k, v in ame_json.items():
            if k not in ignore:
                setattr(amenity, k, v)
        models.storage.save()
        return jsonify(amenity.to_dict())

    if req.method == 'DELETE':
        amenity.delete()
        models.storage.save()
        return jsonify({})
