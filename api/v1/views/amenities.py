#!/usr/bin/python3
"""This is the amenities api module"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Amenity
"""These are the imported modules and packages used"""


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """Retrieves a list of all Amenity objects"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route("/amenities/<amenity_id>", methods = ["GET"])
def get_amenity_by_id(amenity_id):
    """Retrieves an Amenity object by ID"""
    amenity=storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>",
                   methods = ["DELETE"],
                   strict_slashes=False
                   )
def delete_amenity_by_id(amenity_id):
    """Deletes an Amenity object by ID"""
    amenity=storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities", methods = ["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity"""
    data=request.get_json()
    if not data:
        abort(400, description = "Not a JSON")
    if "name" not in data:
        abort(400, description = "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods = ["PUT"],
                                            strict_slashes = False)
def update_amenity_by_id(amenity_id):
    """Updates an Amenity object by ID"""
    amenity=storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data=request.get_json()
    if not data:
        abort(400, description = "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return (jsonify(amenity.to_dict()), 200)
