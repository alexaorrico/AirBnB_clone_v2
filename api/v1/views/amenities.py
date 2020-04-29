#!/usr/bin/python3
"""
View for Amenity objects that handles
all default RestFul API actions.
"""

from flask import Flask, render_template
from api.v1.views import app_views
from models import storage, amenity
from flask import jsonify, abort, request
import models


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    all_amenities = storage.all('Amenity').values()
    list_amenities = []

    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_id(amenity_id):
    """Retrieves the list of specific amenities"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """Deletes an Amenity"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """Creates an Amenity"""
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'message': 'Missing name'}), 400

    amenity = amenity.Amenity(name=request.get_json().get('name'))
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """Updates an Amenity"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
