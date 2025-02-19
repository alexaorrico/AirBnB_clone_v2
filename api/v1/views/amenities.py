#!/usr/bin/python3
"""amenity.py"""

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities")
def get_amenities():
    """retrieves all amenities """
    amenities = []
    amenities_obj = storage.all(Amenity)
    for amenity_obj in amenities_obj.values():
        amenities.append(amenity_obj.to_dict())

    return jsonify(amenities), 200


@app_views.route("/amenities/<string:amenity_id>")
def get_amenity(amenity_id=None):
    """retrieves a specific amenity """
    if amenity_id is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """retrieves a specific amenity """
    if amenity_id is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route("/amenities/", methods=['POST'])
def create_amenity():
    """ Creates a amenity"""
    amenity_dict = None
    try:
        amenity_dict = request.get_json()
    except Exception:
        if not isinstance(amenity_dict, dict):
            return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in amenity_dict:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(name=amenity_dict['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id=None):
    """ updates a amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_dict = None
    try:
        amenity_dict = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, val in amenity_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)

    storage.save()
    return jsonify(amenity.to_dict()), 200
