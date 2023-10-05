#!/usr/bin/python3
"""A new view for Amenity objects that handles all default
RESTFUL API actions"""
from flask import Flask, jsonify, request, abort
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenity():
    """Retrives all Amenity objects"""
    amenities = [a.to_dict() for a in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_based_on_id(amenity_id):
    """Retrives an Amenity object given it's id
    else return 404"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_object(amenity_id):
    """Deletes an Amenity object if found otherwise return 404"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity_object():
    """Creates an Amenity object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object based on the amenity id"""
    fetch_amenity = storage.get(Amenity, amenity_id)
    if fetch_amenity:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        keep = ["id", "created_at", "updated_at"]
        for key, values in data.items():
            if key not in keep:
                setattr(fetch_amenity, key, values)
        fetch_amenity.save()
        return jsonify(fetch_amenity.to_dict()), 200
    else:
        abort(404)
