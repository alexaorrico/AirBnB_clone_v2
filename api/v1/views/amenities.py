#!/usr/bin/python3
"""Routes for amenities objects"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.amenity import Amenity


@app_views.route('amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """get all the amenities  objects"""
    data = storage.all('Amenity')
    new = [value.to_dict() for key, value in data.items()]
    return jsonify(new)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """return each amenity"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Delete each amenity"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """create the amenity if not exists """
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in args:
        return jsonify({"error": "Missing name"}), 400
    obj = Amenity(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id=None):
    """Update each amenity """
    obj = storage.get("Amenity", amenity_id)
    if obj in None:
        abort(404)
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in args.items():
        if key in ["id", "update_at", "created_at"]:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict()), 200
