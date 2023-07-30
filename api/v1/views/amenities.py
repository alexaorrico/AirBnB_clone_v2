#!/usr/bin/python3

"""Handles all default RESTFul API Actions for amenities"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.errorhandler(400)
def handle_400(e):
    """Handle 400 (bad request)"""
    return make_response(jsonify(error=str(e)), 400)


@app_views.route('/api/v1/amenities', strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects from storage"""
    amenities_obj = storage.all("Amenity")
    return jsonify([amenity.to_dict() for amenity in amenities_obj.values()])


@app_views.route('/api/v1/amenities/<amenity_id>', strict_slashes=False)
def get_amenites_by_id(amenity_id):
    """Retrieves a Amenity object from storage with it ID"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/api/v1/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deletes a Amenity object by it ID"""
    amenity = storage.get('Amenity', amenity_id)

    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/amenities', methods=["POST"],
                 strict_slashes=False)
def post_amenities():
    """Creates a Amenity in storage"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    if "name" not in amenity_data:
        abort(400, "Missing name")
    amenity_obj = Amenity(**amenity_data)
    amenity_obj.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Takes an id and update the amenity with the id"""
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    update_data = request.get_json()
    if not update_data:
        abort(400, "Not a JSON")
    for key, val in update_data.items():
        if key not in ignore_keys:
            setattr(amenity, key, val)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
