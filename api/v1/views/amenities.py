#!/usr/bin/python3
"""Defines all routes for the `Amenity` entity
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, classes


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """Returns all amenities in json response"""
    amenities = []
    amenities_objs = storage.all("Amenity")
    for amenity in amenities_objs.values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/", methods=["POST"])
def create_amenity():
    """Creates a new amenity in storage"""
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")
    if "name" not in data:
        return abort(400, description="Missing name")
    amenity = classes["Amenity"](**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """Returns a amenity object or None if not found."""
    amenity = storage.get("Amenity", amenity_id)
    return jsonify(amenity.to_dict()) if amenity else abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes a amenity object from storage"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Update a amenity object by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        return abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("updated_at", None)
    data.pop("created_at", None)

    for k, v in data.items():
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
