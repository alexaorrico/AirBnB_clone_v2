#!/usr/bin/python3
"""Functions handling amenities objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Obtain the information regarding amenities"""
    amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenites_id(amenity_id):
    """Get amenity information for specified amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity based on amenity id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create a new amenity object"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if 'name' not in new_amenity:
        abort(400, "Missing name")
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Update amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(404, "Not a JSON")
    
    for k, v n body_request.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(amenity, k, v)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
