#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 14:42:23 2020
@authors: Robinson Montes
          Mauricio Olarte
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """Create a new view for Amenity objects that handles all default
    RestFul API actions.
    """
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in storage.all('Amenity')
                        .values()])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        new_amenity = Amenity(**post)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_amenity_id(amenity_id):
    """Retrieves a amenity object with a specific id"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        amenity = storage.get('Amenity', amenity_id)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
                storage.save()
        return jsonify(amenity.to_dict()), 200
