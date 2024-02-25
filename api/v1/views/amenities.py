#!/usr/bin/python3
"""Amenities hanlders."""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieve all the amenities."""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["GET"], strict_slashes=False
)
def get_amenity(amenity_id):
    """Get info about specified amenity."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["DELETE"], strict_slashes=False
)
def delete_amenity(amenity_id):
    """Delete specified amenity."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create a new amenity."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    if "name" not in req:
        abort(400, "Missing name")
    amenity = Amenity(**req)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["PUT"], strict_slashes=False
)
def update_amenity(amenity_id):
    """Update specified amenity."""
    req = request.get_json(silent=True)
    if not req:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in ["id", "created_at", "updated_at"]:
            setattr(amenity, attr, val)
    amenity.save()
    return jsonify(amenity.to_dict())
