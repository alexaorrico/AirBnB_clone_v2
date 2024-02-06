#!/usr/bin/python3
"""Handles all RESTful API actions for Amenity"""

from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities")
def amenities():
    """Retrieve list of all Amenity objects."""
    amenities = storage.all(Amenity)
    result = []

    for amenity in amenities.values():
        result.append(amenity.to_dict())

    return jsonify(result)


@app_views.route("/amenities/<amenity_id>")
def amenity(amenity_id):
    """Retrieve one Amenity."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete an amenity."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """Create an amenity."""
    payload = request.get_json()
    if not payload:
        abort(400, "Request body is not a valid JSON")
    if "name" not in payload:
        abort(400, "Payload is missing the 'name' key")

    amenity = Amenity(**payload)
    amenity.save()

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Update an amenity."""
    amenity = storage.get(Amenity, amenity_id)
    payload = request.get_json()
    if not amenity:
        abort(404)
    if not payload:
        abort(400, "Request body is not a valid JSON")

    key = "name"
    setattr(amenity, key, payload[key])
    amenity.save()

    return jsonify(amenity.to_dict())
