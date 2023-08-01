#!/usr/bin/python3
"""
handles REST API actions for Amenity
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
from flask import request
from flask import abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenity():
    """handles amenities route"""
    if request.method == 'GET':
        return jsonify(
            [obj.to_dict() for obj in storage.all("Amenity").values()])
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None or type(post_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        new_name = post_data.get('name')
        if new_name is None:
            return jsonify({'error': 'Missing name'}), 400
        new_amenity = Ameninity(**post_data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    '/amenities/<string:amenity_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False)
def amenity_with_id(amenity_id):
    """handles amenities route with a parameter amenity_id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        put_data = request.get_json()
        if put_data is None or type(put_data) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        to_ignore = ['id', 'created_at', 'updated_at']
        amenity.update(to_ignore, **put_data)
        return jsonify(amenity.to_dict()), 200
