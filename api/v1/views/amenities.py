#!/usr/bin/python3
"""
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_():
    """
    """
    amenities = storage.all("Amenity")
    amenities = [i.to_dict() for i in amenities.values()]
    return (jsonify(amenities))


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def _amenity(amenity_id=None):
    """
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def amenity_delete(amenity_id=None):
    """
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_create():
    """
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    instance = Amenity(**request.get_json())
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def amenity_update(amenity_id):
    """
    """
    key = ['id', 'created_at', 'updated_at']
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for keys, value in request.get_json().items():
        if keys in key:
            pass
        else:
            setattr(amenity, keys, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200