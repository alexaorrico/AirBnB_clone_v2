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


@app_views.route('/amenities/', strict_slashes=False,
                 methods=['GET'])
def get_amenities():
    """Retrieves a list of all amenity objects."""
    amenity_objs = storage.all('Amenity')
    amenities = [obj.to_dict() for obj in amenity_objs.values()]

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a Amenity object."""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_Amenity(amenity_id):
    """Deletes a specified Amenity model."""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route('/amenities/', methods=['POST'])
def create_Amenity():
    """Creates a new Amenity object."""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request.get_json().keys():
        return make_response(jsonify(_{'error': 'Missing name'}), 400)

    amenity = (Amenity(**request.get_json()))
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slaches=False,
                 methods=["PUT"])
def update_Amenity(amenity_id):
    """Modifies a Amenity object."""
    amenity = storage.get('Amenity', amenity_id)

    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 404)

    amenity = amenity_objs.get(amenity_id)
    ignored_keys = ['id', 'created_at', 'updated_at']
    for k, v in request.get_json().items():
        if k not in ignored_keys:
            setattr(amenity, k, v)
    amenity.save()

    return amenity.to_dict()
