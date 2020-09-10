#!/usr/bin/python3
"""Amenity Api Module"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.city import City
from flask import abort
from flask import make_response
from flask import request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """return all amenity in states id"""
    all_amenitys = []
    for obj in storage.all(Amenity).values():
        all_amenitys.append(obj.to_dict())
    return jsonify(all_amenitys)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def aminities_get(amenity_id):
    """Get a specific Amenity object through the HTTP GET request"""
    if amenity_id:
        obj_amenities = storage.get(Amenity, amenity_id)
        if obj_amenities:
            return jsonify(obj_amenities.to_dict())
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def amenities_delete(amenity_id):
    """Delete a specific Amenity object through the HTTP DELETE request"""
    if amenity_id:
        obj_amenities = storage.get(Amenity, amenity_id)
        if obj_amenities:
            storage.delete(obj_amenities)
            storage.save()
            return make_response(jsonify({}), 200)
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def amenities_post():
    """Create a new Amenity object through the HTTP POST request"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenities = Amenity(**req)
    amenities.save()
    return make_response(jsonify(amenities.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def amenities_put(amenity_id):
    """Update a specific Amenity object through the HTTP PUT request"""
    if amenity_id:
        obj_amenities = storage.get(Amenity, amenity_id)
        if obj_amenities is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj_amenities, key, value)
        obj_amenities.save()
        return make_response(jsonify(obj_amenities.to_dict()), 200)
