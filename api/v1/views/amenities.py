#!/usr/bin/python3

"""Handles all default RESTFul API Actions for amenities"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects from storage"""
    amenities_obj = storage.all("Amenity")
    return jsonify(([amenity.to_dict() for amenity in amenities_obj.values()]))


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenites_by_id(amenity_id):
    """Retrieves a Amenity object from storage with it ID"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deletes a Amenity object by it ID"""
    amenity = storage.get('Amenity', amenity_id)

    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=["POST"],
                 strict_slashes=False)
def post_amenities():
    """Creates a Amenity in storage"""
    if not request.get_json():
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity_obj = Amenity(**request.get_json())
    amenity_obj.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Takes an id and update the amenity with the id"""
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    update_data = request.get_json()
    if not update_data:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for key, val in update_data.items():
        if key not in ignore_keys:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict())
