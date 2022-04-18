#!/usr/bin/python3
"""Amenity view model"""
from wsgiref.validate import validator
from flask import abort
from flask import jsonify
from flask import request
from flask import make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

amenity_objs = storage.all('Amenity')


@app_views.route('/amenities/', methods=['GET'])
def get_amenities():
    """Retrieves a list of all amenity objects."""
    amenities = [obj.to_dict() for obj in amenity_objs.values()]

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a Amenity object."""
    amenity_id = "Amenity." + amenity_id

    if amenity_id not in amenity_objs.keys():
        abort(404)

    amenity = amenity_objs.get(amenity_id)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_Amenity(amenity_id):
    """Deletes a specified Amenity model."""
    amenity_id = "Amenity." + amenity_id

    if amenity_id not in amenity_objs.keys():
        abort(404)

    storage.delete()
    storage.save()

    return jsonify({})

@app_views.route('/amenities/', methods=['POST'])
def create_Amenity():
    """Creates a new Amenity object."""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, 'Missing name')

    amenity = (Amenity(**request.get_json()))
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_Amenity(amenity_id):
    """Modifies a Amenity object."""
    amenity_objs = storage.all('Amenity')
    amenity_id = "Amenity." + amenity_id

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 404)
    if amenity_id not in amenity_objs.keys():
        abort(404)

    amenity = amenity_objs.get(amenity_id)
    ignored_keys = ['id', 'created_at', 'updated_at']
    for k, v in request.get_json().items():
        if k not in ignored_keys:
            setattr(amenity, k, v)
    amenity.save()

    return amenity.to_dict()