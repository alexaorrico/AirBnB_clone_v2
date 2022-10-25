#!/usr/bin/python3
""" This module retrieves amenity objects
"""

from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """This method gets all instances of state"""
    amenities_list = storage.all("Amenity")
    all_amenities = []
    for obj in amenities_list.values():
        all_amenities.append(obj.to_dict())
    return jsonify(all_amenities)


@app_views.route(
    "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False
    )
def get_amenity_by_id(amenity_id):
    """This function get the state by its id."""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, "Not found")
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False
    )
def delete_amenity_by_id(amenity_id):
    """This function delete_amenity_by_id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, "Not found")
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenities_by_id():
    """This function creates a new state"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Name is missing")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save
    return make_response(amenity.to_dict(), 201)


@app_views.route(
    "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False
    )
def update_amenity_by_id(amenity_id):
    """This function updates amenity by its id."""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, "Not found")
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    ignore_list = ["id", "created_at", "updated_at"]
    for key, value in new_amenity.items():
        if key not in ignore_list:
            setattr(amenity, key, value)
        amenity.save()
        storage.save()
    return jsonify(amenity.to_dict()), 200
