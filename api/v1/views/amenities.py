#!/usr/bin/python3
"""RESTful API functions for Amenity"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import request, jsonify, abort


@app_views.route("/amenities",
                 strict_slashes=False,
                 methods=["GET", "POST"])
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def amenity_end_points(amenity_id=None):
    """Handles all default RESTful API actions for amenity objects"""
    amenities = storage.all(Amenity).values()

    if not amenity_id:
        if request.method == "GET":
            amenities_dict = [amenity.to_dict() for amenity in amenities]
            return jsonify(amenities_dict)

        elif request.method == "POST":
            data = request.get_json()
            if not data or not isinstance(data, dict):
                abort(400, "Not a JSON")
            if "name" not in data:
                abort(400, "Missing name")

            new_amenity = Amenity(**data)
            new_amenity.save()
            return jsonify(new_amenity.to_dict()), 201
    else:
        amenity = next(
                (amenity for amenity in
                    amenities if amenity.id == amenity_id), None)
        if not amenity:
            abort(404)

        if request.method == "GET":
            return jsonify(amenity.to_dict())

        elif request.method == "DELETE":
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200

        elif request.method == "PUT":
            data = request.get_json()
            if not data or not isinstance(data, dict):
                abort(400, "Not a JSON")

            if "name" in data:
                amenity.name = data["name"]
            amenity.save()
            return jsonify(amenity.to_dict()), 200
