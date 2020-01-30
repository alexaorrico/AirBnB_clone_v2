#!/usr/bin/python3
"""
Defines Amenity endpoints
"""
from models import storage
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_all_amenities():
    """Gets all Amenities."""
    amenity_dict = storage.all("Amenity")
    return jsonify([amenity.to_dict() for amenity in amenity_dict.values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """Gets an Amenity by id."""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return amenity.to_dict()


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity."""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}, 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenities():
    """Creates an Amenity."""
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    if "name" not in json_data:
        return "Missing name", 400
    new_amenity = Amenity(**json_data)
    new_amenity.save()
    return new_amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity."""
    ignore = ["id", "created_at", "updated_at"]
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        return "Not a JSON", 400
    for key, value in json_data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return amenity.to_dict(), 200
