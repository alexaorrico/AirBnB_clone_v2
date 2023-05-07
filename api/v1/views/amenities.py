#!/usr/bin/python3
"""
amenities view routes
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route(
    "/amenities",
    methods=["GET", "POST"],
    strict_slashes=False,
)
def amenities():
    """Handles /amenities endpoint

    Returns:
        json: list of all amenities or the newly added amenity
    """
    if request.method == "POST":
        amenity_data = request.get_json(silent=True)
        if amenity_data is None:
            return jsonify(error="Not a JSON"), 400

        if "name" not in amenity_data:
            return jsonify(error="Missing name"), 400
        else:
            amenity = Amenity(**amenity_data)
            storage.new(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201

    else:
        amenities = list(storage.all(Amenity).values())
        return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False,
)
def amenity(amenity_id=None):
    """Handles /amenities/amenity_id endpoint

    Returns:
        json: object for GET, empty dict for DELETE or 404
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    elif request.method == "PUT":
        amenity_data = request.get_json(silent=True)
        if amenity_data is None:
            return jsonify(error="Not a JSON"), 400

        for key, value in amenity_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())

    else:
        return jsonify(amenity.to_dict())
