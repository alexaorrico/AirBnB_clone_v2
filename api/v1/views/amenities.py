#!/usr/bin/python3
"""Amenity RESTAPI"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():  # Get all amenities
    amenities = storage.all(Amenity)
    return jsonify([value.to_dict() for _, value in amenities.items()])


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):  # get a specific amenity
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_amenity(amenity_id):  # Delete a city
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():  # Create an amenity
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["PUT"])
def update_amenity(amenity_id):  # Update a state
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    abort(404)
